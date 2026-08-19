# 🤖 Smart Shop Assistant

An AI-powered agent designed to process customer queries dynamically, distinguishing between general chat and real-time product/inventory lookup tools using Function Calling.

Built as part of the **Scaler AI Engineering** series.

---

## 🌟 Key Features

* **Autonomous Tool Selection:** Uses an LLM execution loop to intelligently decide *when* to execute a backend tool versus when to handle queries using standard conversational context.
* **Product & Price Lookup:** Dynamically fetches inventory data and pricing upon request.
* **Interactive Web Interface:** Clean UI powered by Gradio for real-time testing and user interaction.

---

## 🏗️ Architecture & How It Works

The core design follows the **LLM + Tool + Loop** pattern:
