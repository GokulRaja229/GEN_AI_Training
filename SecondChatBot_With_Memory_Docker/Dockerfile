FROM python:3.12-slim
WORKDIR /SecondChatBot_With_Memory
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY . .
EXPOSE 8501
CMD ["python", "-m", "streamlit","run","chatbot.py","--server.port=8501","--server.address=0.0.0","--server.headless=true"]
