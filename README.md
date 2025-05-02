
# 🍽️ Find Restaurants

A full-stack application that allows users to search for nearby restaurants using natural language queries. The project integrates React (frontend), FastAPI (backend), and a Hugging Face LLM model.

---

### **Backend**

- **Language & Framework:**  
  Python, FastAPI

- **LLM Integration:**  
  - Library: Hugging Face Transformers  
  - Model: `mistralai/Mistral-7B-Instruct-v0.1`

---

### **Frontend**

- **Framework:**  
  ReactJS

---

### **Setup Guide (Tested on macOS)**

#### 🛠 Clone the repository

```bash
git clone https://github.com/rave-25/Find-Restaurants.git
cd Find-Restaurants
```

---

#### 📦 Backend Setup

```bash
cd backend
```

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your Foursquare API key:
   ```
   FOURSQUARE_KEY=fsq3kF+n2tk1BXAEWIPb3x0l5Yg/vp8DM//0cBBC4ty8aqE=
   ```

4. Run the FastAPI server:
   ```bash
   fastapi dev app/
   ```

---

#### 💻 Frontend Setup

```bash
cd frontend
```

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

---

### ✅ Enjoy!

Open your browser and start exploring restaurant recommendations powered by an LLM!
