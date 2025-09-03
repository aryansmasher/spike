# app.py ▸ BEBOP (Spike chat • CI/CD • HTML gallery)
# ────────────────────────────────────────────────────────────
import os, ssl, subprocess, tempfile, webbrowser
import streamlit as st
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from openai import OpenAI

# ───────── CONFIG ─────────
AWS_REGION = "ap-south-1"
SPIKE_KEY  = "AIzaSyDXEXI5AHS7G1MOcCifDTGV27lNVa7GGrQ"   # move to env var for prod
OPENAI_BASE= "https://generativelanguage.googleapis.com/v1beta/openai/"
REPO_URL   = "https://github.com/aryansmasher/devops_project_1"

# ───────── THEME & TITLE ─────────
st.set_page_config("BEBOP", "🚀", layout="wide")
st.markdown("""
<style>
  html,body{background:#0d1117;color:#e6edf3}
  h1,h2,h3{color:#e50914}
  section [data-testid="stButton"]>button{background:#e50914;color:#fff}
</style>
""", unsafe_allow_html=True)
st.title("🚀 BEBOP – Spike Edition")

# ───────── SPIKE CHAT ─────────
spike = OpenAI(api_key=SPIKE_KEY, base_url=OPENAI_BASE)
def spike_chat(prompt:str)->str:
    msgs=[{"role":"system","content":"You are Spike Spiegel from Cowboy Bebop — be unhinged."},
          {"role":"user","content":prompt}]
    return spike.chat.completions.create(model="gemini-2.5-flash",messages=msgs).choices[0].message.content

# ───────── AWS CLIENTS ─────────
ec2=s3=None
try:
    sess=boto3.Session(region_name=AWS_REGION)
    ec2,s3=sess.client("ec2"),sess.client("s3")
except (BotoCoreError,ClientError) as err:
    st.warning(f"AWS init failed: {err}")

# ───────── HTML GALLERY ─────────
def html_gallery()->None:
    if not os.path.exists("html_pages"):
        st.info("Create an 'html_pages' folder and add your HTML files.")
        return
    files=sorted(f for f in os.listdir("html_pages") if f.endswith(".html"))
    if not files:
        st.info("No HTML files found in 'html_pages'.")
        return
    page=st.selectbox("Choose an HTML page",files,key="html_select")
    height=st.slider("Iframe height",200,1_000,500,50,key="html_height")
    with open(os.path.join("html_pages",page),"r",encoding="utf-8") as f:
        st.components.v1.html(f.read(),height=height,scrolling=True)

# ───────── NAVIGATION ─────────
menu=[
    "Spike Chat","AWS Cloud","Web Tools","Python Tasks",
    "Docker Dashboard","HTML Pages","My Portfolio","CI/CD Pipeline ↗"
]
section=st.sidebar.radio("Jump to section",menu)
st.sidebar.divider()
if st.sidebar.button("Open Portfolio"):
    webbrowser.open_new_tab("https://aryancodes.netlify.app")
if st.sidebar.button("Open Repo / CI Config"):
    webbrowser.open_new_tab(REPO_URL)

# ═════════ 1 SPIKE CHAT ═════════
if section=="Spike Chat":
    st.header("Spike Spiegel – Unhinged Assistant")
    if "history" not in st.session_state: st.session_state.history=[]
    user=st.chat_input("Say something to Spike…")
    if user:
        with st.spinner("Loading jazz…"):
            reply=spike_chat(user)
            st.session_state.history.extend([("user",user),("assistant",reply)])
    for role,msg in st.session_state.history:
        with st.chat_message(role): st.markdown(msg)

# ═════════ 2 AWS CLOUD ═════════
elif section=="AWS Cloud":
    st.header("AWS Cloud Utilities")
    task=st.selectbox("Choose task",["List S3 buckets","List EC2 instances"])
    if task=="List S3 buckets" and st.button("Run"):
        st.write([b["Name"] for b in s3.list_buckets().get("Buckets",[])] if s3 else "S3 client unavailable")
    elif task=="List EC2 instances" and st.button("Run"):
        if ec2:
            ids=[i["InstanceId"] for r in ec2.describe_instances().get("Reservations",[])
                                   for i in r.get("Instances",[])]
            st.write(ids or "No instances")
        else:
            st.error("EC2 client unavailable")

# ═════════ 3 WEB TOOLS ═════════
elif section=="Web Tools":
    st.header("Web Utilities")
    import requests,bs4
    tool=st.selectbox("Choose tool",["HTTP Status","Page Title"])
    url=st.text_input("URL")
    if tool=="HTTP Status" and st.button("Check"):
        try: st.write(requests.get(url,timeout=5).status_code)
        except Exception as e: st.error(e)
    elif tool=="Page Title" and st.button("Fetch"):
        try:
            title=bs4.BeautifulSoup(requests.get(url,timeout=5).text,"html.parser").title
            st.write(title.string if title else "No <title>")
        except Exception as e:
            st.error(e)

# ═════════ 4 PYTHON TASKS ═════════
elif section=="Python Tasks":
    st.header("Python Tasks Hub")
    task=st.selectbox("Select task",[
        "Create Image","Download Website Links","Google Search",
        "LinkedIn Message","Send Email","Send SMS",
        "Make Call","WhatsApp Message","Face-Swap (demo)"
    ])
    def missing(p): st.error(f"Install {p} to use this feature.")

    if task=="Create Image":
        from PIL import Image,ImageDraw
        txt,clr=st.text_input("Text"),st.color_picker("Background","#0000FF")
        if st.button("Create"):
            img=Image.new("RGB",(400,200),color=clr)
            ImageDraw.Draw(img).text((20,90),txt,fill="white")
            tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".png"); img.save(tmp.name)
            st.image(tmp.name); st.download_button("Download",open(tmp.name,"rb"),"output.png")

    elif task=="Download Website Links":
        url=st.text_input("URL")
        if st.button("Scrape"):
            try:
                soup=bs4.BeautifulSoup(requests.get(url,timeout=10).text,"html.parser")
                links=sorted({a["href"] for a in soup.find_all("a",href=True)})
                st.write(f"{len(links)} links:"); st.write("\n".join(links))
            except Exception as e: st.error(e)

    elif task=="Google Search":
        try:
            from googlesearch import search
            q=st.text_input("Query"); n=st.slider("Results",1,20,10)
            if st.button("Search"):
                [st.write(f"{i}. {l}") for i,l in enumerate(search(q,num_results=n),1)]
        except ImportError: missing("googlesearch-python")

    elif task=="LinkedIn Message":
        try:
            from linkedin_api import Linkedin
            email,pw,uid,msg=(st.text_input("Email"),
                              st.text_input("Password",type="password"),
                              st.text_input("Recipient ID"),
                              st.text_area("Message"))
            if st.button("Send"): Linkedin(email,pw).send_message(uid,msg); st.success("Sent")
        except ImportError: missing("linkedin-api")

    elif task=="Send Email":
        import smtplib; from email.message import EmailMessage
        sender,pw,to,subj,body=(st.text_input("Gmail"),
                                st.text_input("App password",type="password"),
                                st.text_input("Recipient"),
                                st.text_input("Subject"),
                                st.text_area("Body"))
        if st.button("Send Email"):
            msg=EmailMessage(); msg.set_content(body); msg["Subject"],msg["From"],msg["To"]=subj,sender,to
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com",465,context=ssl.create_default_context()) as s:
                    s.login(sender,pw); s.send_message(msg)
                st.success("Email sent")
            except Exception as e:
                st.error(e)

    elif task=="Send SMS":
        try:
            from twilio.rest import Client
            sid,tok,frm,to,body=(st.text_input("SID"),
                                 st.text_input("Auth token",type="password"),
                                 st.text_input("Twilio #"),
                                 st.text_input("Recipient #"),
                                 st.text_area("Body"))
            if st.button("Send SMS"):
                sid_out=Client(sid,tok).messages.create(body=body,from_=frm,to=to).sid
                st.success(f"Sent (SID {sid_out})")
        except ImportError: missing("twilio")

    elif task=="Make Call":
        try:
            from twilio.rest import Client
            sid,tok,frm,to=(st.text_input("SID"),
                            st.text_input("Auth token",type="password"),
                            st.text_input("Twilio #"),
                            st.text_input("Recipient #"))
            if st.button("Call"):
                sid_out=Client(sid,tok).calls.create(
                    twiml="<Response><Say>Hello from Spike!</Say></Response>",to=to,from_=frm).sid
                st.success(f"Call started (SID {sid_out})")
        except ImportError: missing("twilio")

    elif task=="WhatsApp Message":
        try:
            import pywhatkit as kit
            phone,msg=st.text_input("WhatsApp # +cc"),st.text_area("Message")
            if st.button("Send"): kit.sendwhatmsg_instantly(phone,msg,wait_time=15); st.success("Queued")
        except ImportError: missing("pywhatkit")

    else:
        st.info("Add your OpenCV/dlib face-swap logic here.")

# ═════════ 5 DOCKER DASHBOARD ═════════
elif section=="Docker Dashboard":
    st.header("Docker Dashboard")
    choice=st.selectbox("Operation",[
        "Select","Launch Container","Stop Container","Remove Container",
        "Start Container","List Images"
    ])
    def run(cmd): st.code(subprocess.run(cmd,shell=True,capture_output=True,
                                         text=True).stdout or "Done")
    if choice=="Launch Container":
        name,img=st.text_input("Name"),st.text_input("Image (e.g., nginx)")
        if st.button("Run"): run(f"docker run -dit --name {name} {img}"); st.success("Launched")
    elif choice=="Stop Container":
        name=st.text_input("Name"); st.button("Stop",on_click=lambda:run(f"docker stop {name}"))
    elif choice=="Remove Container":
        name=st.text_input("Name"); st.button("Remove",on_click=lambda:run(f"docker rm -f {name}"))
    elif choice=="Start Container":
        name=st.text_input("Name"); st.button("Start",on_click=lambda:run(f"docker start {name}"))
    elif choice=="List Images" and st.button("List"):
        run("docker images")

# ═════════ 6 CI/CD PIPELINE ═════════
elif section=="CI/CD Pipeline ↗":
    st.header("CI/CD Pipeline for devops_project_1")
    st.markdown(f"""
* Repository: **[aryansmasher/devops_project_1]({REPO_URL})**  
* Workflow file: `.github/workflows/ci-cd.yml`  
* Push to **main** (or open a PR) and GitHub Actions will test, build, push & deploy.
""")
    st.code("""name: CI-CD Pipeline
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
env:
  DOCKER_REPO: aryansmasher/devops_project_1
jobs:
  test-build-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.12'}
      - run: pip install -e .[dev]
      - run: pytest -q
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USER }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_REPO }}:latest
            ${{ env.DOCKER_REPO }}:${{ github.sha }}""",language="yaml")

# ═════════ 7 HTML PAGES ═════════
elif section=="HTML Pages":
    st.header("Static & Interactive HTML Pages")
    html_gallery()

# ───────── FOOTER ─────────
st.divider()
st.caption("©2025 BEBOP • See you, space cowboy…")
