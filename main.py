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

fmt=3
url_args=""

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
    if "key_systems" in video_source and fmt == 3:
        widevine_url = video_source["key_systems"]["com.widevine.alpha"][
            "license_url"
        ]
        microsoft_url = video_source["key_systems"]["com.microsoft.playready"][
            "license_url"
        ]

    track_url = video["text_tracks"][1]["src"]
    if url_args != "fastly_token=NjE3YWZjYjZfMmIzMTI3YmU5MzNhOTljOTM2ZGUyZDZjNDNhMGJhNTQ5ZGU2ODdiMWZhZTgwZjhlMDQ2ZGQyYzg0ZGZiMzlkZg%3D%3D&bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2NpZCI6IjYyMDY0NTkxMjMwMDEiLCJleHAiOjE2MzU0NDU5OTcsImlhdCI6MTYzNTQ0MTE5NywiY29uaWQiOiI2Mjc4ODY1MzA2MDAxIiwibWF4aXAiOjF9.Iqxn5TfvXxESIBWvjaEHvDh875kAOEUNrIEnPZHPPl_XCreNJKqdmiwUsr_GkIKDiZRrvthcY9jQENhRtkHNaBX1h-R6LaAXyVRxYsz1eeBFN9ykY-mmMZDDPS8o0mdoHb17lAJCFKDrdPqc5uP7unElpU8DsX904reraYpV8eUEzMHA0vEHWSy_Os9dpc43og_A73-4EqFfIdGGOXgY4UTd8fJ5DHBAx-YF1l77BqVHiHXQmMyCQ1rXtN0T7LlCj3UF9e2RCwgEOiI45wnt_HS-LmYD1igk-5N45bseuqjO40nnmvSAlsIVPa6JweEARuHSgsCa9gvSoSN69ThI2g":
        video_url += "?" + url_args
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
