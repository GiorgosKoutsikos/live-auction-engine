# ⚡ Real-Time Live Auction Engine

A lightweight, high-performance real-time live auction engine built from scratch with **FastAPI**, **WebSockets**, and **SQLite**.

---

## 🎯 Project Overview

This project simulates a live bidding platform. When a bidder submits a higher offer, the server validates the incoming bid against the SQLite database, commits the updated price and bid history, and immediately broadcasts the change to all connected clients in real time using persistent WebSocket connections.

---

## 🚀 Key Features

- **Real-time Bid Broadcasting**: Instant state updates pushed to all active clients simultaneously via WebSockets.
- **Persistent Relational Storage**: Full persistence for auctions and individual bids using SQLite (`auctions.db`) with foreign key constraints.
- **Initial State Hydration**: Automatically syncs newly connected clients with the latest auction state on connection.
- **Bid Validation**: Enforces business logic requiring incoming bids to exceed the current highest offer.
- **Minimal Dark-mode UI**: Clean, responsive frontend for placing bids and seeing live price changes.

---

## 🧠 What I Learned

Building this project provided hands-on, end-to-end backend and real-time networking experience:

- **Real-Time WebSockets**: Designing a custom `ConnectionManager` class in FastAPI to handle client connection lifecycles (`connect`, `disconnect`) and broadcast payloads across active connections.
- **Relational Database Design & SQL**: Structuring tables with foreign keys (`auctions`, `bids`), executing parameterized queries (`INSERT`, `UPDATE`, `SELECT`) in `sqlite3` to prevent SQL injection, and managing transactions (`conn.commit()`).
- **Bid Validation & Concurrency**: Validating incoming real-time payloads against current database state before accepting price increments.
- **Frontend-Backend Integration**: Establishing two-way browser communication using the native JavaScript `WebSocket` API and dynamically updating the DOM without page refreshes.
- **Project Hygiene & Git**: Maintaining clean repository structure, managing `.gitignore` for local SQLite databases, and structuring descriptive Git commits.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, WebSockets
- **Database**: SQLite3
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (WebSocket API)

---

## ⚙️ Installation & Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/live-auction-engine.git
   cd live-auction-engine

   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python database.py
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
