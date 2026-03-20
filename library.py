from abc import ABC, abstractmethod
import pickle

class Book:
    def __init__(self, title, author, status):
        self.__title = title
        self.__author = author
        self.__status = status
    
    def getTitle(self):
        return self.__title
    
    def getAuthor(self):
        return self.__author
    
    def getStatus(self):
        return self.__status
    
    def setStatus(self, status):
        self.__status = status
    
    def toFileString(self):
        return f"{self.__title};{self.__author};{self.__status}\n"
    
    @staticmethod
    def fromFileString(line):
        title, author, statusStr = line.strip().split(";")
        status = statusStr == "True"
        return Book(title, author, status)

class Person(ABC):
    def __init__(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    @abstractmethod
    def getRole(self):
        pass

class Librarian(Person):
    def __init__(self, name):
        super().__init__(name)
    
    def getRole(self):
        return "librarian"
    
    @staticmethod
    def fromFileString(line):
        return Librarian(line.strip())

class LibraryUser(Person):
    def __init__(self, name):
        super().__init__(name)
        self.__borrowedBooks = []
    
    def getRole(self):
        return "user"
    
    def getBorrowedBooks(self):
        return self.__borrowedBooks.copy()
    
    def borrowBook(self, book):
        self.__borrowedBooks.append(book)
    
    def returnBook(self, bookTitle):
        for book in self.__borrowedBooks:
            if(book.getTitle() == bookTitle):
                self.__borrowedBooks.remove(book)
                return True
        return False
    
    def toFileString(self):
        result = f"{self.getName()}\n"
        for book in self.__borrowedBooks:
            result += book.toFileString()
        return result
    
    @staticmethod
    def fromFileLines(lines):
        if(len(lines) == 0):
            return None
        user = LibraryUser(lines[0].strip())
        for i in range(1, len(lines)):
            if(lines[i].strip()):
                user.borrowBook(Book.fromFileString(lines[i]))
        return user

class LibrarySystem:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.__librarians = [Librarian("admin")]
        self.__currentUser = None
    
    def addBook(self, book):
        self.__books.append(book)
    
    def removeBook(self, index):
        if(0 <= index < len(self.__books)):
            return self.__books.pop(index)
        return None
    
    def getBooks(self):
        return self.__books.copy()
    
    def getAvailableBooks(self):
        available = []
        for book in self.__books:
            if(book.getStatus()):
                available.append(book)
        return available
    
    def findBookByTitle(self, title):
        for book in self.__books:
            if(book.getTitle() == title):
                return book
        return None
    
    def addUser(self, user):
        self.__users.append(user)
    
    def removeUser(self, name):
        for i in range(len(self.__users)):
            if(self.__users[i].getName() == name):
                return self.__users.pop(i)
        return None
    
    def getUsers(self):
        return self.__users.copy()
    
    def findUser(self, name):
        for user in self.__users:
            if(user.getName() == name):
                return user
        return None
    
    def getLibrarians(self):
        return self.__librarians.copy()
    
    def findLibrarian(self, name):
        for librarian in self.__librarians:
            if(librarian.getName() == name):
                return librarian
        return None
    
    def setCurrentUser(self, user):
        self.__currentUser = user
    
    def getCurrentUser(self):
        return self.__currentUser
    
    def saveData(self):
        try:
            with open("library_data.pkl", "wb") as file:
                pickle.dump({
                    'books': self.__books,
                    'users': self.__users,
                    'librarians': self.__librarians
                }, file)
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def loadData(self):
        try:
            with open("library_data.pkl", "rb") as file:
                data = pickle.load(file)
                self.__books = data.get('books', [])
                self.__users = data.get('users', [])
                self.__librarians = data.get('librarians', [Librarian("admin")])
        except FileNotFoundError:
            self.__books = []
            self.__users = []
            self.__librarians = [Librarian("admin")]
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            self.__books = []
            self.__users = []
            self.__librarians = [Librarian("admin")]

librarySystem = LibrarySystem()
librarySystem.loadData()

if(len(librarySystem.getLibrarians()) == 0):
    librarySystem.addLibrarian(Librarian("admin"))

while(True):
    if(librarySystem.getCurrentUser() == None):
        print("Библиотечная система")
        print("1. Войти как библиотекарь")
        print("2. Войти как пользователь")
        print("3. Выйти")
        
        userInput = input("Выберите действие: ")
        
        if(userInput == "1"):
            librarianName = input("Введите имя библиотекаря: ")
            librarian = librarySystem.findLibrarian(librarianName)
            if(librarian):
                librarySystem.setCurrentUser(librarian)
            else:
                print("Библиотекарь не найден")
        
        elif(userInput == "2"):
            userName = input("Введите имя пользователя: ")
            user = librarySystem.findUser(userName)
            if(user):
                librarySystem.setCurrentUser(user)
            else:
                print("Пользователь не найден")
        
        elif(userInput == "3"):
            librarySystem.saveData()
            print("Данные сохранены. До свидания!")
            break
    
    elif(librarySystem.getCurrentUser().getRole() == "librarian"):
        print("Меню библиотекаря")
        print("1. Добавить новую книгу")
        print("2. Удалить книгу")
        print("3. Зарегистрировать нового пользователя")
        print("4. Просмотреть список всех пользователей")
        print("5. Просмотреть список всех книг")
        print("6. Вернуться в главное меню")
        
        userInput = input("Выберите действие: ")
        
        if(userInput == "1"):
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            newBook = Book(title, author, True)
            librarySystem.addBook(newBook)
            print("Книга успешно добавлена")
        
        elif(userInput == "2"):
            books = librarySystem.getBooks()
            if(len(books) == 0):
                print("В библиотеке нет книг")
            else:
                print("Список книг:")
                for i in range(len(books)):
                    statusText = "доступна" if(books[i].getStatus()) else "выдана"
                    print(f"{i+1}. {books[i].getTitle()} - {books[i].getAuthor()} ({statusText})")
                
                try:
                    bookIndex = int(input("Введите номер книги для удаления: ")) - 1
                    removedBook = librarySystem.removeBook(bookIndex)
                    if(removedBook):
                        print(f"Книга '{removedBook.getTitle()}' удалена")
                    else:
                        print("Неверный номер книги")
                except ValueError:
                    print("Введите корректное число")
        
        elif(userInput == "3"):
            userName = input("Введите имя нового пользователя: ")
            existingUser = librarySystem.findUser(userName)
            if(existingUser):
                print("Пользователь с таким именем уже существует")
            else:
                newUser = LibraryUser(userName)
                librarySystem.addUser(newUser)
                print(f"Пользователь '{userName}' успешно зарегистрирован")
        
        elif(userInput == "4"):
            users = librarySystem.getUsers()
            if(len(users) == 0):
                print("Нет зарегистрированных пользователей")
            else:
                print("Список пользователей:")
                for i in range(len(users)):
                    print(f"{i+1}. {users[i].getName()}")
        
        elif(userInput == "5"):
            books = librarySystem.getBooks()
            if(len(books) == 0):
                print("В библиотеке нет книг")
            else:
                print("Список всех книг:")
                for i in range(len(books)):
                    statusText = "доступна" if(books[i].getStatus()) else "выдана"
                    print(f"{i+1}. {books[i].getTitle()} - {books[i].getAuthor()} ({statusText})")
        
        elif(userInput == "6"):
            librarySystem.setCurrentUser(None)
    
    elif(librarySystem.getCurrentUser().getRole() == "user"):
        currentUser = librarySystem.getCurrentUser()
        print(f"Меню пользователя ({currentUser.getName()})")
        print("1. Просмотреть доступные книги")
        print("2. Взять книгу")
        print("3. Вернуть книгу")
        print("4. Просмотреть список взятых книг")
        print("5. Вернуться в главное меню")
        
        userInput = input("Выберите действие: ")
        
        if(userInput == "1"):
            availableBooks = librarySystem.getAvailableBooks()
            if(len(availableBooks) == 0):
                print("Нет доступных книг")
            else:
                print("Доступные книги:")
                for i in range(len(availableBooks)):
                    print(f"{i+1}. {availableBooks[i].getTitle()} - {availableBooks[i].getAuthor()}")
        
        elif(userInput == "2"):
            availableBooks = librarySystem.getAvailableBooks()
            if(len(availableBooks) == 0):
                print("Нет доступных книг для взятия")
            else:
                print("Доступные книги:")
                for i in range(len(availableBooks)):
                    print(f"{i+1}. {availableBooks[i].getTitle()} - {availableBooks[i].getAuthor()}")
                
                bookTitle = input("Введите название книги, которую хотите взять: ")
                book = librarySystem.findBookByTitle(bookTitle)
                
                if(book):
                    if(book.getStatus()):
                        book.setStatus(False)
                        currentUser.borrowBook(Book(book.getTitle(), book.getAuthor(), False))
                        print(f"Вы взяли книгу '{bookTitle}'")
                    else:
                        print("Эта книга уже выдана")
                else:
                    print("Книга не найдена")
        
        elif(userInput == "3"):
            borrowedBooks = currentUser.getBorrowedBooks()
            if(len(borrowedBooks) == 0):
                print("У вас нет взятых книг")
            else:
                print("Ваши взятые книги:")
                for i in range(len(borrowedBooks)):
                    print(f"{i+1}. {borrowedBooks[i].getTitle()} - {borrowedBooks[i].getAuthor()}")
                
                bookTitle = input("Введите название книги, которую хотите вернуть: ")
                
                if(currentUser.returnBook(bookTitle)):
                    book = librarySystem.findBookByTitle(bookTitle)
                    if(book):
                        book.setStatus(True)
                    print(f"Вы вернули книгу '{bookTitle}'")
                else:
                    print("У вас нет такой книги")
        
        elif(userInput == "4"):
            borrowedBooks = currentUser.getBorrowedBooks()
            if(len(borrowedBooks) == 0):
                print("У вас нет взятых книг")
            else:
                print("Ваши взятые книги:")
                for i in range(len(borrowedBooks)):
                    print(f"{i+1}. {borrowedBooks[i].getTitle()} - {borrowedBooks[i].getAuthor()}")
        
        elif(userInput == "5"):
            librarySystem.setCurrentUser(None)