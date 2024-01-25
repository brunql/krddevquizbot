
QUESTIONS = [
  {
    "question": "Прочитали правила клуба?",
    "options": ["Нет", "Правильный ответ - ДА (идет в зачет)", "Нажми меня", "Вот же!"],
    "correct_option_number": 2
  },
  {
    "question": "Каких JOIN не бывает?",
    "options": ["INNER", "CROSS", "FULL", "OUT"],
    "correct_option_number": 4
  },
  {
    "question": "Пишем CRUD, кто лишний?",
    "options": ["INSERT", "DELETE", "ALTER", "UPDATE"],
    "correct_option_number": 3
  },
  {
    "question": "Волшебная команда git для путешествия по времени и багам?",
    "options": ["git switch -c past/42/future", "git reflog", "git bisect", "git log"],
    "correct_option_number": 3
  },
  {
    "question": "Как создать коммит для аннигиляции изменений предыдущего?",
    "options": ["git revert HEAD", "git reset --mixed HEAD~1", "git diff HEAD~1 HEAD", "git rebase master"],
    "correct_option_number": 1
  },
  {
    "question": "Оторвалась голова, что делать?",
    "options": ["git log", "git checkout master", "git revert HEAD", "git clone"],
    "correct_option_number": 2
  },
  {
    "question": "Потеряли коммит в объектной БД, ссылок на него нет, где искать?",
    "options": ["git reflog", "git log -S deadbeef", "git grep -i -n deadbeef", "git log --grep deadbeef"],
    "correct_option_number": 1
  },
  {
    "question": "Как проверить информацию о дистрибутиве?",
    "options": ["lscpu", "lsb_release -a", "lsb_release -c", "lsblk"],
    "correct_option_number": 2
  },
  {
    "question": "Что делает команда “cd -”?",
    "options": ["Переход в домашнюю папку", "Просмотр каталога", "Переход в предыдущую папку", "Выход из системы"],
    "correct_option_number": 3
  },
  {
    "question": "Как получить последние 10 команд?",
    "options": ["history | tail", "history | head", "cat ~/.bash-hist | tail", "free -m | grep history: | awk {print $4}"],
    "correct_option_number": 1
  },
  {
    "question": "Как попасть в веб-интерфейс на удаленном хосте по 8080 порту через ssh?",
    "options": ["ssh -L 8080:localhost:8080 user@domain.net", "ssh -p 8080 user@domain.net", "scp user@domain.net:8080:/a /b", "ssh -N 8080 user@domain.net"],
    "correct_option_number": 1
  },
  {
    "question": "PHP-разраба попросили поправить JS-скрипт, как бы отмазался Валера?",
    "options": ["К сожалению занят, пиво выбираю", "К сожалению занят, пиво пью", "Я слишком стар для этого дерьма", "Жира таскс оверфлоу"],
    "correct_option_number": 2
  },
  {
    "question": "Сколько паттернов разработки знает Валера?",
    "options": ["10", "23", "5", "1"],
    "correct_option_number": 2
  },
  {
    "question": "Что из перечисленного отсылает к шаблонам проектирования?",
    "options": ["KISS", "YAGNY", "GRASP", "DRY"],
    "correct_option_number": 3
  },
  {
    "question": "Какой принцип скрывается под аббревиатурой DI?",
    "options": ["Data In", "Dependency Inversion", "Dependency Injection", "Discrete Input"],
    "correct_option_number": 2
  },
  {
    "question": "Зачем нужен TURN-сервер для WebRTC?",
    "options": ["Помогает устройствам, находящимся за NAT определить внешний IP адрес роутера", "Помогает установить канал связи между двумя клиентами и обеспечивает транзит трафика через себя", "Организует обмен SDP между клиентами", "Мониторинг качества соединений по аудио-видео связи"],
    "correct_option_number": 2
  },
  {
    "question": "Предположим, Валера хочет отправить Марку секретное сообщение, каким протоколом им следует воспользоваться для подготовки секретного ключа?",
    "options": ["ICMP", "Протоколом Диффи-Хеллмана", "HTTP", "NTP"],
    "correct_option_number": 2
  },
]
