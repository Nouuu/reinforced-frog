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
VOLUME /app/qtable

ENV AGENT_LEARNING_FILE='qtable/qtable.data' \
    AGENT_LEARNING_RATE=0.6 \
    AGENT_GAMMA=0.8 \
    AGENT_VISIBLE_LINES_ABOVE=2 \
    AGENT_VISIBLE_COLS_ARROUND=20 \
    AGENT_QTABLE_HISTORY=2 \
    LEARNING_MODE=True \
    AGENT_DEBUG=False \
    LEARNING_TIME=20 \
    WORLD_TYPE=0

CMD [ "python","-u", "./main.py" ]
