# ⚽ ELITE ARENA | Football League Management System

A Python-based Football League Management System developed using **Object-Oriented Programming (OOP)** and **Streamlit**.

Elite Arena provides an interactive platform for managing football tournaments, registering teams and players, generating match schedules, tracking match results, and calculating league standings automatically.

The project combines a structured OOP backend with a modern, interactive graphical user interface.

---

## 🚀 Project Overview

Elite Arena is designed to simplify football tournament management through an organized and user-friendly system.

The application allows administrators to:

- Register football teams.
- Add players to their respective teams.
- Generate automatic round-robin match schedules.
- Start and finish football matches.
- Record match scores.
- Track yellow and red cards.
- Calculate league standings automatically.
- Display tournament statistics through an interactive dashboard.

---

## ✨ Key Features

### 1. Team Management
- Register new football teams.
- Assign unique team IDs.
- Prevent duplicate team registrations.
- Manage team activity status.
- Track the number of registered players.

### 2. Player Management
- Add players to teams.
- Assign player roles:
  - Goalkeeper
  - Defender
  - Midfielder
  - Forward
- Prevent duplicate player IDs within the same team.
- Manage player banning and unbanning.

### 3. Match Management
- Automatically generate tournament fixtures.
- Start upcoming matches.
- Record final match scores.
- Track match statuses:
  - Upcoming
  - Live
  - Finished
- Determine match winners and draws.

### 4. Football Card System
- Record yellow cards.
- Record direct red cards.
- Automatically issue a red card when a player receives two yellow cards.
- Prevent banned or sent-off players from receiving additional cards.

### 5. League Standings
Automatically calculate:

| Statistic | Description |
|---|---|
| P | Matches Played |
| W | Matches Won |
| D | Matches Drawn |
| L | Matches Lost |
| GF | Goals For |
| GA | Goals Against |
| GD | Goal Difference |
| PTS | Total Points |

Teams are ranked according to:
1. Total Points.
2. Goal Difference.
3. Goals For.
4. Team Name.

### 6. Interactive Dashboard
The Streamlit interface provides:

- Season overview.
- Registered teams statistics.
- Total fixtures.
- Completed matches.
- Live matches.
- Recent match results.
- Tournament progress.
- Current league standings.

---

## 🏗️ Object-Oriented Programming Concepts

The project demonstrates several fundamental OOP concepts in Python.

### 1. Abstraction
Implemented using the `ABC` module and abstract methods.

Abstract classes:
- `Participant`
- `Match`

Abstract methods:
- `get_info()`
- `get_match_details()`

### 2. Inheritance
Implemented through class relationships:

- `HumanPlayer` inherits from `Participant`.
- `Team` inherits from `Participant`.
- `FootballMatch` inherits from `Match`.

### 3. Encapsulation
Data and related operations are organized within classes.

Examples:
- Player banning and unbanning.
- Team player management.
- Match status management.
- Tournament registration and scheduling.

### 4. Polymorphism
Different classes implement their own versions of abstract methods, such as `get_info()` and `get_match_details()`.

### 5. Composition
The system connects multiple objects:

- A Tournament contains teams and matches.
- A Team contains players.
- A FootballMatch connects two teams.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OOP | Application architecture |
| Streamlit | Graphical User Interface |
| Pandas | Data organization and tables |
| Datetime | Date and time utilities |
| HTML & CSS | Interface customization |

---

## 📂 Project Structure

```text
elite-arena-football-league-manager/
│
├── main.py              # OOP classes and core business logic
│
├── streamlit_app.py     # Streamlit graphical interface
│
├── requirements.txt     # Project dependencies
│
└── README.md            # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmed7Ayman/elite-arena-football-league-manager.git
```

### 2. Navigate to the Project Directory

```bash
cd elite-arena-football-league-manager
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run streamlit_app.py
```

The application will open automatically in your browser.

If it does not, open:

```text
http://localhost:8501
```

---

## 📦 Requirements

The project requires:

```text
streamlit
pandas
```

Install them using:

```bash
pip install streamlit pandas
```

---

## 🖥️ Application Navigation

The application contains five main sections:

| Section | Function |
|---|---|
| Dashboard | Overview of tournament statistics |
| Fixtures | Manage matches and record results |
| Standings | Display automatically calculated rankings |
| Teams & Players | Manage teams and player rosters |
| Manage League | Register teams and generate fixtures |

---

## ⚽ Tournament Scheduling Logic

Elite Arena uses a **Single Round-Robin Tournament System**.

Every active team plays against every other active team exactly once.

The total number of matches is calculated using:

\[
Matches = \frac{n(n-1)}{2}
\]

Where `n` represents the number of active teams.

For example:

- 2 teams = 1 match.
- 3 teams = 3 matches.
- 4 teams = 6 matches.
- 5 teams = 10 matches.

---

## 🔒 Data Validation & Error Handling

The system includes validation mechanisms to maintain data consistency.

Examples include:

- Preventing empty participant names and IDs.
- Preventing duplicate team registrations.
- Preventing duplicate player IDs within a team.
- Preventing a team from playing against itself.
- Ensuring matches follow the correct status sequence.
- Validating match scores as non-negative integers.
- Preventing banned players from participating in card events.
- Preventing schedule generation more than once.

---

## 🔮 Future Improvements

Potential future development includes:

- Database integration (SQLite / MySQL).
- User authentication and administrator roles.
- Persistent tournament storage.
- Match dates and venue management.
- Player statistics and performance tracking.
- Advanced tournament formats.
- Exporting league standings to Excel and PDF.
- Live match updates.
- Player transfer management.

---

## 👨‍💻 Author

**Developed as a Python Object-Oriented Programming Project.**

### ELITE ARENA
*Manage Your League. Track Every Match. Own the Competition.*

---

## 📄 License

This project is available for educational and development purposes.
