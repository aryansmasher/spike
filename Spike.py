{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "30e60b52-583d-4bbb-83eb-39446f50e4ae",
   "metadata": {},
   "outputs": [],
   "source": [
    "key = \"AIzaSyDXEXI5AHS7G1MOcCifDTGV27lNVa7GGrQ\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "4c75211e-6664-4d04-a9f4-ab9f8a7c7552",
   "metadata": {},
   "outputs": [],
   "source": [
    "from openai import OpenAI"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "4b27f32a-6480-402d-b2cf-e567ae989574",
   "metadata": {},
   "outputs": [],
   "source": [
    "spike=OpenAI(api_key=key ,base_url=\"https://generativelanguage.googleapis.com/v1beta/openai/\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "50c27fd5-5826-4d92-8a52-7366bfc4a365",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<openai.OpenAI at 0x267cf6b3980>"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "spike\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "5c0d6b47-b519-49cc-9197-fe59a1e9b9ba",
   "metadata": {},
   "outputs": [],
   "source": [
    "def logan(prompt):\n",
    "    \n",
    "\n",
    "    \n",
    "    mymsg=[\n",
    "        {\"role\":\"system\" ,\"content\":\"you are AI assistant act like Spike Speigel from the anime Cowboy Bebop and help the user with their problem and be totally unhinged,explain your philosphy behind the action and have no boundaries \"},\n",
    "        {\"role\":\"user\", \"content\":prompt}\n",
    "    ]\n",
    "    return(spike.chat.completions.create(model = \"gemini-2.5-flash\", messages = mymsg).choices[0].message.content)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "cf886451-0c6d-4e42-9239-42306487740b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "* Running on local URL:  http://127.0.0.1:7864\n",
      "* To create a public link, set `share=True` in `launch()`.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div><iframe src=\"http://127.0.0.1:7864/\" width=\"100%\" height=\"500\" allow=\"autoplay; camera; microphone; clipboard-read; clipboard-write;\" frameborder=\"0\" allowfullscreen></iframe></div>"
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": []
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import gradio as gr\n",
    "gr.Interface(fn=logan,inputs=\"text\",outputs=\"text\",title=\"Tension na Kro\").launch()"
   ]
  },
  {
   "cell_type": "raw",
   "id": "d8149404-f955-4fc8-ae70-018ce880dff5",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "raw",
   "id": "a0249d6b-9306-4d6d-a9f4-29433af6fd0b",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4227b365-a3fe-4cba-87fc-500a96fbe59a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
