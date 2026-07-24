# 🍔 Hardee's AI Voice Ordering Assistant

An AI-powered voice assistant for **Hardee's Restaurant** built using **LiveKit Agents**, **Groq LLM**, **Deepgram Speech-to-Text**, **Cartesia Text-to-Speech**, and **Retrieval-Augmented Generation (RAG)**.

The assistant allows customers to naturally interact with the restaurant over voice or chat to:

- 🍔 Place food orders
- 📖 Browse the restaurant menu
- 🔍 Search menu items using semantic search
- 🪑 Reserve restaurant tables
- 💳 Handle payment methods
- 💰 Enforce advance payment rules for large COD orders

---

# Features

## 🍔 AI Food Ordering

Customers can order naturally, for example:

> "I'd like two Zinger Burgers and a large fries."

The assistant will:

- Search the menu if necessary
- Add items to the cart
- Show the current order
- Calculate totals
- Confirm the order

---

## 🔍 Smart Menu Search (RAG)

Instead of relying on keyword matching, the assistant uses semantic search with **Sentence Transformers**.

Example:

User:

> "Show me something spicy."

The assistant understands the intent and returns relevant menu items even if the exact words don't exist in the menu.

---

## 🪑 Restaurant Reservation

The assistant can book tables by collecting:

- Customer name
- Reservation date
- Reservation time
- Number of guests

After gathering the information, it confirms the reservation.

---

## 💳 Payment Handling

Supports:

- Cash on Delivery (COD)
- Card Payment

Business rule:

- Orders above **5000 PKR**
- Require a **minimum advance payment of 1500 PKR** if the customer chooses COD.

---

## 🛒 Shopping Cart

The assistant keeps track of:

- Ordered items
- Quantities
- Estimated total

---

## 🎙 Voice Conversation

Powered by:

- Deepgram STT
- Groq LLM
- Cartesia TTS
- LiveKit Agents

The assistant behaves like a real restaurant employee.

---

# Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| LiveKit Agents | Voice Agent Framework |
| Groq | Large Language Model |
| Deepgram | Speech-to-Text |
| Cartesia | Text-to-Speech |
| Sentence Transformers | Semantic Search |
| NumPy | Vector Operations |
| JSON | Menu Database |
| Next.js | Frontend |
| React | User Interface |

---

# Project Structure

```
calling-agent/
│
├── main.py                 # LiveKit agent entry point
├── api.py                  # Restaurant Agent + Function Tools
├── rag.py                  # Semantic menu search
├── menu.json               # Restaurant menu
├── requirements.txt
│
├── my-voice-gui/
│   ├── app/
│   ├── components/
│   ├── public/
│   └── ...
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/hardees-ai-assistant.git

cd hardees-ai-assistant
```

---

## Create Virtual Environment

Windows

```bash
python -m venv ai

ai\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv ai

source ai/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example:

```env
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=

DEEPGRAM_API_KEY=

GROQ_API_KEY=

CARTESIA_API_KEY=
```

---

# Running the Backend

```bash
python main.py dev
```

or

```bash
lk agent dev
```

---

# Running the Frontend

Navigate to the GUI project.

```bash
cd my-voice-gui
```

Install packages.

```bash
pnpm install
```

Start the frontend.

```bash
pnpm dev
```

Open

```
http://localhost:3000
```

---

# Example Conversation

**User**

> I'd like a burger.

↓

Assistant searches the menu.

↓

User

> Add one Super Star Burger.

↓

Assistant

> Added one Super Star Burger.

↓

User

> Also give me fries.

↓

Assistant

> Added Curly Fries.

↓

User

> That's all.

↓

Assistant

> Your estimated total is 1130 PKR.
Would you like delivery or pickup?

---

# Reservation Example

User

> I'd like to reserve a table.

Assistant

> Certainly! May I have your name?

↓

User

> John

↓

Assistant

> What date would you like to reserve?

↓

User

> Tomorrow

↓

Assistant

> What time?

↓

User

> 8 PM

↓

Assistant

> How many guests?

↓

User

> Four

↓

Assistant

> Your reservation has been confirmed.

---

# Current Functionality

- Voice conversation
- Menu search using embeddings
- Order management
- Shopping cart
- Reservation system
- Payment handling
- Advance payment validation
- LiveKit integration
- Next.js frontend

---

# Planned Features

- Interactive graphical menu
- Live shopping cart
- Item recommendations
- Combo meal suggestions
- Nutrition information
- Order history
- Customer authentication
- Delivery tracking
- Promotional offers
- Loyalty rewards

---

# Future GUI

The planned interface includes:

- AI Assistant panel
- Live conversation window
- Scrollable restaurant menu
- Category navigation
- Recommended food section
- Smart menu highlighting
- Animated shopping cart
- Real-time order summary

---

# Author

**Wasiq Sulaman**

Computer Engineering Student

COMSATS University Islamabad, Lahore Campus

Interested in:

- Artificial Intelligence
- Agentic AI
- Voice Agents
- Machine Learning
- Database Systems
- Embedded Systems

---
