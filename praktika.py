import time
import serial
import pyfirmata

long_stopwatch = 0
        # long_stopwatch - (длинный_секндомер) -
        # это секундомер, который реализуется через time.sleep
        # нужен, чтобы засекать допустимое время наполнения чаши до проверки
        
current_stopwatch = 0
        # current_stopwatch - (текущий_секундомер)
        # эта переменная нужна, чтобы изменить работу long_stopwatch
        # в случае, если проверка покажет, что очищать чашу пока не от чего
# зададим список датчиков
detector_list = []
print("Хотите начать работу аппарата? Введите 1, если хотите начать работу программы, и 0, если не хотите")
answer = int(input()) 

        if answer == 1: 
                 #включить порт
                 board = pyfirmata.Arduino('Ваш Порт Здесь')
                 print("Соединение Успешно Установлено")

                 #начать работу чаши
                 long_stopwatch = timing(long_stopwatch)
                 # то, что время закончилось, означает, что пора проверить,
                 # нужно ли чистить чашу (устраиваем проверку)
                  Liquid_Sensor_Answer = checking()
                          if Liquid_Sensor_Answer != 0 :
                                 #если проверка показала, что нужно чистить, то
                                  cleaning()
                                  return 0
                          else :
                                 #если проверка показала, что чистить еще нечего
                                  long_stopwatch = current_stopwatch
                                  long_stopwatch = timing(long_stopwatch)
                                  return 0

         
         #если ответ 0 (нет), то завершаем работу программы            
         elif answer == 0: 
                    return 0

         # в интерфейсе программы 1- это будет да, 0- нет,
         # /но если каким-то образом пользователь нажимает не туда,
         # то просим ввести данные корректно
         else:
                 return "Введите 1 ,если хотите начать работу программы, и 0, если не хотите"
        


def cleaning():
         #закрыть крышку
                cover.digital[13].write(1)
                time.sleep(30)
                cover.digital[13].write(0)
                time.sleep(1)
         # высосать жидкость
                  bloody_liquid_out.digital[13].write(1)
                  time.sleep(60)
                  bloody_liquid_out.digital[13].write(0)
                  time.sleep(1)       
         # дезинфекция
                 desinfection.digital[13].write(1)
                 time.sleep(180)
                 desinfection.digital[13].write(0)
                 time.sleep(1)
         # высосать дезинфицирующую жидкость
                 desinfection_liquid_out.digital[13].write(1)
                 time.sleep(60)
                 desinfection_liquid_out .digital[13].write(0)
                 time.sleep(1)
         # запустить длинный_секундомер заново
                 long_stopwatch = 0
         #закончить работу функции очистки
                 return 0
        
               

def checking():
        it = pyfirmata.util.Iterator(board)
        it.start()

        board.digital[10].mode = pyfirmata.input

        while True:
            sw = board.digital[10].read()
            if sw is True:
                board.digital[13].write(1)
            else:
                board.digital[13].write(0)
            time.sleep(0.1)
        pin1 = board.get_pin('d:3:p')
        return pin1

def timing(timer):
        while timer < 10800: # Засекаю время того, сколько чаша может заполняться,
                             # обычно это около 4 часов, взяла 3 с запасом, это 10800 секунд 
                time.sleep(1)
                timer += 1
                return timer
        
