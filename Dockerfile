FROM python:3.10

RUN apt-get update \
  && apt-get install -y -qq --no-install-recommends \
    libxext6 \
    libx11-6 \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    freeglut3-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
VOLUME /app/save

ENV AGENT_COUNT=5 \
    AGENT_DEBUG=false \
    ARCADE_INSIGHTS=true \
    AGENT_GAMMA=0.1 \
    AGENT_LEARNING_FILE='save/qtable_l2c4.xz' \
    AGENT_LEARNING_RATE=0.6 \
    AGENT_VISIBLE_COLS_ARROUND=4 \
    AGENT_VISIBLE_LINES_ABOVE=2 \
    EXPLORE_RATE=-1 \
    EXPLORE_RATE_DECAY=0.999 \
    GENERATE_HISTORY_GRAPH=true \
    HASH_QTABLE=false \
    LEARNING_MODE=true \
    LEARNING_TYPE=QLEARNING \
    LEARNING_TIME=600 \
    LEARNING_PRINT_STATS_EVERY=60 \
    LEARNING_SAVE_QTABLE_EVERY=300 \
    QTABLE_HISTORY_FILE='save/qtable_l2c4.history' \
    QTABLE_HISTORY_PACKETS=10 \
    WORLD_TYPE=0


CMD [ "python","-u", "./main.py" ]
