from typing import List, Optional
from src.buch.entity.buch_entity import Book, BookCreate, BookUpdate
from src.buch.entity.autor_entity import Autor, AutorCreate, AutorUpdate
from src.buch.entity.verlag_entity import Verlag, VerlagCreate, VerlagUpdate


class AutorMockRepo:
    def __init__(self):
        self._autoren: List[Autor] = [
            Autor(id=1, name="Saint-Exupéry", vorname="Antoine de", geburtsjahr=1900, nationalitaet="Französisch"),
            Autor(id=2, name="Goethe", vorname="Johann Wolfgang von", geburtsjahr=1749, nationalitaet="Deutsch"),
        ]
        self._next = 3

    def get_all(self) -> List[Autor]:
        return self._autoren

    def get_by_id(self, autor_id: int) -> Optional[Autor]:
        for a in self._autoren:
            if a.id == autor_id:
                return a
        return None

    def create(self, autor_in: AutorCreate) -> Autor:
        autor = Autor(id=self._next, **autor_in.model_dump())
        self._autoren.append(autor)
        self._next += 1
        return autor

    def update(self, autor_id: int, autor_in: AutorCreate) -> Optional[Autor]:
        autor = self.get_by_id(autor_id)
        if not autor:
            return None

        autor.name = autor_in.name
        autor.vorname = autor_in.vorname
        autor.geburtsjahr = autor_in.geburtsjahr
        autor.nationalitaet = autor_in.nationalitaet
        return autor

    def patch(self, autor_id: int, autor_in: AutorUpdate) -> Optional[Autor]:
        autor = self.get_by_id(autor_id)
        if not autor:
            return None

        if autor_in.name is not None:
            autor.name = autor_in.name
        if autor_in.vorname is not None:
            autor.vorname = autor_in.vorname
        if autor_in.geburtsjahr is not None:
            autor.geburtsjahr = autor_in.geburtsjahr
        if autor_in.nationalitaet is not None:
            autor.nationalitaet = autor_in.nationalitaet
        return autor

    def delete(self, autor_id: int) -> bool:
        for i, autor in enumerate(self._autoren):
            if autor.id == autor_id:
                self._autoren.pop(i)
                return True
        return False


class VerlagMockRepo:
    def __init__(self):
        self._verlage: List[Verlag] = [
            Verlag(id=1, name="Gallimard", stadt="Paris", land="Frankreich", gruendungsjahr=1911),
            Verlag(id=2, name="Suhrkamp", stadt="Frankfurt am Main", land="Deutschland", gruendungsjahr=1950),
        ]
        self._next = 3

    def get_all(self) -> List[Verlag]:
        return self._verlage

    def get_by_id(self, verlag_id: int) -> Optional[Verlag]:
        for v in self._verlage:
            if v.id == verlag_id:
                return v
        return None

    def create(self, verlag_in: VerlagCreate) -> Verlag:
        verlag = Verlag(id=self._next, **verlag_in.model_dump())
        self._verlage.append(verlag)
        self._next += 1
        return verlag

    def update(self, verlag_id: int, verlag_in: VerlagCreate) -> Optional[Verlag]:
        verlag = self.get_by_id(verlag_id)
        if not verlag:
            return None

        verlag.name = verlag_in.name
        verlag.stadt = verlag_in.stadt
        verlag.land = verlag_in.land
        verlag.gruendungsjahr = verlag_in.gruendungsjahr
        return verlag

    def patch(self, verlag_id: int, verlag_in: VerlagUpdate) -> Optional[Verlag]:
        verlag = self.get_by_id(verlag_id)
        if not verlag:
            return None

        if verlag_in.name is not None:
            verlag.name = verlag_in.name
        if verlag_in.stadt is not None:
            verlag.stadt = verlag_in.stadt
        if verlag_in.land is not None:
            verlag.land = verlag_in.land
        if verlag_in.gruendungsjahr is not None:
            verlag.gruendungsjahr = verlag_in.gruendungsjahr
        return verlag

    def delete(self, verlag_id: int) -> bool:
        for i, verlag in enumerate(self._verlage):
            if verlag.id == verlag_id:
                self._verlage.pop(i)
                return True
        return False


class BookMockRepo:
    def __init__(self, autor_repo: AutorMockRepo, verlag_repo: VerlagMockRepo):
        self.autor_repo = autor_repo
        self.verlag_repo = verlag_repo
        
        autor1 = autor_repo.get_by_id(1)
        verlag1 = verlag_repo.get_by_id(1)
        autor2 = autor_repo.get_by_id(2)
        verlag2 = verlag_repo.get_by_id(2)

        if not autor1 or not verlag1 or not autor2 or not verlag2:
            raise ValueError("Initial data for Autor or Verlag fehlt")

        self._books: List[Book] = [
            Book(
                id=1,
                title="Der kleine Prinz",
                autor=autor1,
                verlag=verlag1,
                description="Klassiker",
                publikationsjahr=1943,
            ),
            Book(
                id=2,
                title="Faust",
                autor=autor2,
                verlag=verlag2,
                description="Drama",
                publikationsjahr=1808,
            ),
        ]
        self._next = 3

    def get_all(self) -> List[Book]:
        return self._books

    def get_by_id(self, book_id: int) -> Optional[Book]:
        for b in self._books:
            if b.id == book_id:
                return b
        return None

    def create(self, book_in: BookCreate) -> Book:
        autor = self.autor_repo.get_by_id(book_in.autor_id)
        verlag = self.verlag_repo.get_by_id(book_in.verlag_id)
        
        if not autor or not verlag:
            raise ValueError("Autor oder Verlag nicht gefunden")
        
        book = Book(
            id=self._next, 
            title=book_in.title, 
            autor=autor,
            verlag=verlag,
            description=book_in.description,
            publikationsjahr=book_in.publikationsjahr
        )
        self._books.append(book)
        self._next += 1
        return book

    def update(self, book_id: int, book_in: BookCreate) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            return None
        
        autor = self.autor_repo.get_by_id(book_in.autor_id)
        verlag = self.verlag_repo.get_by_id(book_in.verlag_id)
        
        if not autor or not verlag:
            raise ValueError("Autor oder Verlag nicht gefunden")
        
        book.title = book_in.title
        book.autor = autor
        book.verlag = verlag
        book.description = book_in.description
        book.publikationsjahr = book_in.publikationsjahr
        return book

    def patch(self, book_id: int, book_in: BookUpdate) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            return None
        if book_in.title is not None:
            book.title = book_in.title
        if hasattr(book_in, 'autor_id') and book_in.autor_id is not None:
            autor = self.autor_repo.get_by_id(book_in.autor_id)
            if not autor:
                raise ValueError("Autor nicht gefunden")
            book.autor = autor
        if hasattr(book_in, 'verlag_id') and book_in.verlag_id is not None:
            verlag = self.verlag_repo.get_by_id(book_in.verlag_id)
            if not verlag:
                raise ValueError("Verlag nicht gefunden")
            book.verlag = verlag
        if book_in.description is not None:
            book.description = book_in.description
        if hasattr(book_in, 'publikationsjahr') and book_in.publikationsjahr is not None:
            book.publikationsjahr = book_in.publikationsjahr
        return book

    def delete(self, book_id: int) -> bool:
        for i, b in enumerate(self._books):
            if b.id == book_id:
                self._books.pop(i)
                return True
        return False


# Singleton instances
_autor_repo = AutorMockRepo()
_verlag_repo = VerlagMockRepo()
repo = BookMockRepo(_autor_repo, _verlag_repo)
autor_repo = _autor_repo
verlag_repo = _verlag_repo
