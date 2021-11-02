import os
import requests
from flask import Flask
from flask import request
from flask import render_template



ACCOUNT_ID = os.environ.get("ACCOUNT_ID", "6206459123001")
BCOV_POLICY = os.environ.get(
    "BCOV_POLICY",
    "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd",
)

bc_url = (
    f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
)

bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

fmt=4
url_args="bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NpZCI6IjYyMDY0NTkxMjMwMDEiLCJleHAiOjE2MzU2ODY3NDMsImlhdCI6MTYzNTY4MTk0MywiY29uaWQiOiI2Mjc4MzAwMDAxMDAxIiwibWF4aXAiOjF9.MOcr31iKUCmg4fHCgP_j6trU1sbFqKvd2FzWD1VYxw-geQcrQxETV3IidWkcXMm_YsYOZ7z161wRH5DAY9xArIR2n5SIoBYsBnWWWMOn9MEsmSEQ0wHU3izMuzS9GPt1JThMKPclWlxL4NkiL8h-pocN8kzQeFGxMnpRsOAXutgZv9jQq8lDifJH5mgsDRCVsfwHtKea0IjxNBSUHXa8cyDfVN8ojQLeYQbQAnuoW-KAIVpVj5iC_qiY5dDVwwU-jDef95JZuq5Dcndq5DT_Psdz7IoQdMSF3rnh_6mn1adF0EDSYhjPbtr1W7jxupUx5yRKkoSTwDpyif5mlZWHJQ"

jw_url = "https://cdn.jwplayer.com/v2/media"


app = Flask(__name__)


@app.route("/<int(fixed_digits=13):video_id>")
def brightcove(video_id):
    video_response = requests.get(f"{bc_url}/{video_id}", headers=bc_hdr)

    if video_response.status_code != 200:
        return "<font color=red size=20>Wrong Video ID</font>"

    video = video_response.json()

    video_name = video["name"]

    video_source = video["sources"][3]
    video_url = video_source["src"]
    widevine_url = ""
    microsoft_url = ""
    if "key_systems" in video_source and fmt == 4:
        widevine_url = video_source["key_systems"]["com.widevine.alpha"][
            "license_url"
        ]
        microsoft_url = video_source["key_systems"]["com.microsoft.playready"][
            "license_url"
        ]

    track_url = video["text_tracks"][1]["src"]
    if url_args != "bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NpZCI6IjYyMDY0NTkxMjMwMDEiLCJleHAiOjE2MzU2ODY3NDMsImlhdCI6MTYzNTY4MTk0MywiY29uaWQiOiI2Mjc4MzAwMDAxMDAxIiwibWF4aXAiOjF9.MOcr31iKUCmg4fHCgP_j6trU1sbFqKvd2FzWD1VYxw-geQcrQxETV3IidWkcXMm_YsYOZ7z161wRH5DAY9xArIR2n5SIoBYsBnWWWMOn9MEsmSEQ0wHU3izMuzS9GPt1JThMKPclWlxL4NkiL8h-pocN8kzQeFGxMnpRsOAXutgZv9jQq8lDifJH5mgsDRCVsfwHtKea0IjxNBSUHXa8cyDfVN8ojQLeYQbQAnuoW-KAIVpVj5iC_qiY5dDVwwU-jDef95JZuq5Dcndq5DT_Psdz7IoQdMSF3rnh_6mn1adF0EDSYhjPbtr1W7jxupUx5yRKkoSTwDpyif5mlZWHJQ":
        video_url += "&" + url_args
    return render_template(
        "template.html",
        type="brightcove",
        video_name=video_name,
        video_url=video_url,
        track_url=track_url,
        widevine_url=widevine_url,
        microsoft_url=microsoft_url,
    )   
 

@app.route("/<string(length=8):video_id>")
def jw(video_id):
    video_response = requests.get(f"{jw_url}/{video_id}")

    if video_response.status_code != 200:
        return "<font color=red size=20>Wrong Video ID</font>"

    video = video_response.json()

    video_name = video["title"]

    video_url = video["playlist"][0]["sources"][0]["file"]
    track_url = video["playlist"][0]["tracks"][0]["file"]
    return render_template(
        "template.html",
        type="jw",
        video_name=video_name,
        video_url=video_url,
        track_url=track_url,
    )
