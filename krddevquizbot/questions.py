
QUESTIONS = [
  {
    "question": "Прочитали правила клуба?",
    "options": ["Нет", "Правильный ответ - ДА (идет в зачет)", "Нажми меня", "Вот же!"],
    "correct_option_number": 2
  },
  {
    "question": "В каком году вышла первая версия PHP?",
    "options": ["1993", "1995", "1994", "1997"],
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
    "question": "Оторвалась голова, что делать?",
    "options": ["git log", "git checkout master", "git revert HEAD", "git clone"],
    "correct_option_number": 2
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
    "question": "Сколько паттернов разработки должен знать PHP разработчик?",
    "options": ["10", "23", "5", "1"],
    "correct_option_number": 2
  },
  {
    "question": "Что из перечисленного отсылает к шаблонам проектирования?",
    "options": ["KISS", "YAGNY", "GRASP", "DRY"],
    "correct_option_number": 3
  },
  {
    "question": "Какой принцип скрывается под аббревиатурой DIP?",
    "options": ["Data In Principle", "Dependency Inversion Principle", "Dependency Injection Principle", "Discrete Input Protocol"],
    "correct_option_number": 2
  },
  {
    "question": "Предположим, Валера хочет отправить Марку секретное сообщение, каким протоколом им следует воспользоваться для подготовки секретного ключа?",
    "options": ["ICMP", "Протоколом Диффи-Хеллмана", "HTTP", "NTP"],
    "correct_option_number": 2
  },
  {
    "question": "Что будет в переменной $x после выполнения кода $x = 5; $x % 2;",
    "options": ["0", "2", "5", "1"],
    "correct_option_number": 3
  },
  {
    "question": "С помощью какой функции можно удалить Cookie?",
    "options": ["getcookie", "setcookie", "deletecookie", "readcookie"],
    "correct_option_number": 2
  },
  {
    "question": "Что будет в переменной $result после выполнения кода $i = 5; $result = ++$i;?",
    "options": ["6", "5", "4", "7"],
    "correct_option_number": 1
  },
  {
    "question": "С помощью какой функции можно прочитать файл?",
    "options": ["print_r", "file_get_contents", "array_merge", "read_from_file"],
    "correct_option_number": 2
  },
  {
    "question": "Что будет в переменной $result после выполнения кода $result = (true xor true)?",
    "options": ["false", "0", "true", "1"],
    "correct_option_number": 1
  },
  {
    "question": "Что будет в переменной $x после выполнения кода $x = 2 <=> 4;?",
    "options": ["false", "-1", "true", "0"],
    "correct_option_number": 2
  },
  {
    "question": "Продолжит ли код выполнение после выражения require 1.php; если файл 1.php не будет найден?",
    "options": ["да, но выведет ошибку", "да, без каких либо ошибок", "нет, выведет ошибку и завершится", "свой создаст"],
    "correct_option_number": 3
  },
  {
    "question": "Какая функция возвращает максимальное значение памяти, выделенной PHP скрипту?",
    "options": ["memory_limit", "memory_get_max_usage", "memory_get_peak_usage", "memory_get_usage"],
    "correct_option_number": 3
  },
  {
    "question": "Что выведет этот код: echo 0.1 + 0.2 - 0.3; ?",
    "options": ["0", "0.0", "5.5511151231258E-17", "0.0000000001"],
    "correct_option_number": 3
  },
  {
    "question": "Какой из перечисленных методов не является магическим?",
    "options": ["__set", "__clone", "__static", "__invoke"],
    "correct_option_number": 3
  },
]
