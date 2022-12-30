import json
import os
import splittext

SUBTITLE_DIR = "transcribe"
AUDIO_DIR = "audio"
INFO_DIR = "info"
MD_DIR = "md"

def load_json(file):
    with open(file, encoding="utf8") as f:
        data = json.load(f)
        return data
# convert seconds to timestamp in the format of 00:00:00
def seconds_to_timestamp(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)

# return total number of minutes from seconds
def seconds_to_minutes(seconds):
    return seconds // 60

# format date from YYYYMMDD to YYYY-MM-DD
def format_date(date):
    return date[:4] + "-" + date[4:6] + "-" + date[6:]

# generate a file name from string with only alphanumeric and replace space with underscore
def generate_filename(string):
    return "".join(x for x in string if x.isalnum() or x.isspace()).replace(" ", "_")

def create_index():
    # create index.md file
    with open("./" + MD_DIR + "/index.md", "w", encoding="utf8") as f:
        f.write("---\n")
        f.write('| Title | Duration | Date |\n')
        f.write('| ---------- | ------ | ----  |\n')
        for file in os.listdir(AUDIO_DIR):
            if file.endswith(".mp3"):
                info = load_json(INFO_DIR + "/" + file.replace(".mp3",".info.json"))
                title = info["title"]
                duration = seconds_to_minutes(int(info["duration"]))
                upload_date = format_date(info["upload_date"])
                link_to_md = "./{}.md".format(generate_filename(title))
                f.write('| [{}]({}) | {} min | {} |\n'.format(title, link_to_md, duration,upload_date))

# create markdown file
def create_md(title, info, whisper_data):
    # create markdown file
    md_file = generate_filename(title)+".md"

    with open("./" + MD_DIR + "/" + md_file, "w", encoding="utf8") as f:
        youtube_url = info["webpage_url"]
        f.write("---\n")
        f.write('title: "{}"\n\n'.format(title.replace('"',"'")))
        f.write("---\n")
        f.write('=== "Timestamps"\n')
        f.write('    | Timestamp | Text Segment |\n')
        f.write('    | ---------- | ----  |\n')
        

        for segment in whisper_data["segments"]:
            start_url = youtube_url + "&t=" + str(int(segment["start"]))
            end_url = youtube_url + "&t=" + str(int(segment["end"]))
            f.write('    | [{}]({}) | {} |\n'.format(seconds_to_timestamp(segment["start"]),start_url,  segment["text"]))
        
        f.write('\n')
        f.write('=== "Text"\n')
        try:
            text = splittext.split(whisper_data["text"])
        except:
            text = whisper_data["text"]
        text = text.replace("\n\n","<br><br>")
        f.write("    {}".format(text))



def main():
    for file in os.listdir(AUDIO_DIR):
        if file.endswith(".mp3"):
            print(file)
            whisper_json = load_json("./transcribe/"+file.replace(".mp3", ".mp3.json"))
            info_json = load_json("./info/"+file.replace(".mp3", ".info.json"))
            create_md(info_json["title"], info_json, whisper_json)

    create_index()


if __name__ == "__main__":
    main()