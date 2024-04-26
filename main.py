{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 219
    },
    "id": "5VvO3vRJFWK1",
    "outputId": "e43bfc50-e4e8-4c4c-d950-db4d1b0843f0"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n"
     ]
    }
   ],
   "source": [
    "from os import O_TRUNC\n",
    "from flask import Flask,render_template,request\n",
    "import requests\n",
    "import pickle\n",
    "import numpy as np\n",
    "\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "with open(\"C:/Users/bhara/Desktop/PRO/src/Thyroid_model.pkl\",\"rb\") as model_file:\n",
    "    model=pickle.load(model_file)\n",
    "\n",
    "@app.route('/')\n",
    "def index():\n",
    "    return render_template('home.html')\n",
    "\n",
    "@app.route(\"/moreinfo\", methods = [\"GET\", \"POST\"])\n",
    "def moreinfo():\n",
    "    return render_template('moreinfo.html')\n",
    "\n",
    "@app.route(\"/predict\", methods = [\"GET\", \"POST\"])\n",
    "def predict():\n",
    "    return render_template('predict.html')\n",
    "\n",
    "@app.route(\"/predictresult\", methods = [\"GET\", \"POST\"])\n",
    "def predictresult():\n",
    "    if request.method == \"POST\":\n",
    "        Age=float(request.form.get('age'))\n",
    "        Sex= request.form.get('sex')\n",
    "        Level_thyroid_stimulating_hormone= float(request.form.get('TSH'))\n",
    "        Total_thyroxine_TT4= float(request.form.get('TT4'))\n",
    "        Free_thyroxine_index=float(request.form.get('FTI'))\n",
    "        On_thyroxine= request.form.get('on_thyroxine')\n",
    "        On_antithyroid_medication= request.form.get('on_antithyroid_medication')\n",
    "        Goitre= request.form.get('goitre')\n",
    "        Hypopituitary = request.form.get('hypopituitary')\n",
    "        Psychological_symptoms = request.form.get('psych')\n",
    "        T3_measured= request.form.get('T3_measured')\n",
    "\n",
    "\n",
    "        #Sex\n",
    "        if Sex==\"Male\":\n",
    "            Sex=1\n",
    "        else:\n",
    "            Sex=0\n",
    "        #On_thyroxine\n",
    "        if On_thyroxine==\"True\":\n",
    "            On_thyroxine=1\n",
    "        else:\n",
    "            On_thyroxine=0\n",
    "\n",
    "        #On_antithyroid_medication\n",
    "        if On_antithyroid_medication==\"True\":\n",
    "            On_antithyroid_medication=1\n",
    "        else:\n",
    "            On_antithyroid_medication=0\n",
    "\n",
    "        #Goitre\n",
    "        if Goitre==\"True\":\n",
    "            Goitre=1\n",
    "        else:\n",
    "            Goitre=0\n",
    "\n",
    "        #Hypopituitary\n",
    "        if Hypopituitary==\"True\":\n",
    "            Hypopituitary=1\n",
    "        else:\n",
    "            Hypopituitary=0\n",
    "\n",
    "        #Psychological_symptoms\n",
    "        if Psychological_symptoms==\"True\":\n",
    "            Psychological_symptoms=1\n",
    "        else:\n",
    "            Psychological_symptoms=0\n",
    "\n",
    "        #T3_measured\n",
    "        if T3_measured==\"True\":\n",
    "            T3_measured=1\n",
    "        else:\n",
    "            T3_measured=0\n",
    "\n",
    "\n",
    "\n",
    "        arr=np.array([[Age,Sex,Level_thyroid_stimulating_hormone,Total_thyroxine_TT4,Free_thyroxine_index,\n",
    "        On_thyroxine,On_antithyroid_medication,Goitre,Hypopituitary,Psychological_symptoms,T3_measured]])\n",
    "        pred=model.predict(arr)\n",
    "\n",
    "\n",
    "        if pred==0:\n",
    "            res_Val=\"Compensated Hypothyroid\"\n",
    "        elif pred==1:\n",
    "            res_Val=\"No Thyroid\"\n",
    "        elif pred==2:\n",
    "            res_Val='Primary Hypothyroid'\n",
    "        elif pred==3:\n",
    "            res_Val='Secondary Hypothyroid'\n",
    "\n",
    "\n",
    "        Output=f\"Patient has {res_Val}\"\n",
    "        return render_template('predictresult.html',output=Output)\n",
    "\n",
    "\n",
    "    return render_template(\"home.html\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "colab": {
   "provenance": []
  },
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
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
