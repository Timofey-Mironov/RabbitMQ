import pika
import json
import pickle
import time
import numpy as np

# Функция для загрузки модели
def load_model(path="myfile.pkl"):
    # Сериализуем модель
    with open(path, "rb") as pkl_file:
        return pickle.load(pkl_file)

# Функция для обработки входящих сообщений
def callback(ch, method, properties, body):
    # Распаковываем входящее сообщение
    message = json.loads(body)
    message_id = message["id"]
    features = message["body"]

    print(f"Получен вектор признаков (id: {message_id}): {features}")

    # Предсказываем
    pred = regressor.predict(np.array(features).reshape(1, -1))
    # Формируем сообщение с предсказанием
    prediction_message = {"id": message_id, "body": pred[0]}

    # Публикуем предсказание
    ch.basic_publish(
        exchange="", routing_key="y_pred", body=json.dumps(prediction_message)
    )
    print(
        f"Предсказание отправлено в очередь y_pred (id: {message_id}, значение: {pred[0]})"
    )

# Функция для запуска программы
def main():
    while True:
        try:
            # Создаём подключение по адресу rabbitmq:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
            channel = connection.channel()

            # Объявляем очередь features
            channel.queue_declare(queue="features")
            # Объявляем очередь y_pred
            channel.queue_declare(queue="y_pred")

            # Извлекаем сообщение из очереди features
            channel.basic_consume(
                queue="features", on_message_callback=callback, auto_ack=True
            )

            print("...Ожидание сообщений, для выхода нажмите CTRL+C")
            # Запускаем режим ожидания прихода сообщений
            channel.start_consuming()

        # Условия на ограничения
        except KeyboardInterrupt:
            print("Получен сигнал завершения работы")
            if "connection" in locals() and connection.is_open:
                connection.close()
            break

        except Exception as e:
            print(f"Не удалось подключиться к очереди: {str(e)}")
            print("Повторная попытка через 5 секунд...")
            time.sleep(5)
            continue

# Функция для запуска программы из консоли
if __name__ == "__main__":
    # В этом случае прописываем загрузку модели при запуске скрипта
    regressor = load_model()
    main()