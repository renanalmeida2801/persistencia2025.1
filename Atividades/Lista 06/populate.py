from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models.usuario import Usuario
from app.models.post import Post
from app.models.categoria import Categoria
from app.models.comentario import Comentario
from app.models.curtida import Curtida

def popular():
    create_db_and_tables()  # <-- esta linha é essencial

    with Session(engine) as session:
        # Usuários
        u1 = Usuario(nome="Alice", email="alice@example.com", senha="123")
        u2 = Usuario(nome="Bob", email="bob@example.com", senha="456")
        session.add_all([u1, u2])
        session.commit()

        # Categorias
        c1 = Categoria(nome="Tecnologia", descricao="Tudo sobre tech")
        c2 = Categoria(nome="Receitas", descricao="Delícias culinárias")
        session.add_all([c1, c2])
        session.commit()

        # Posts
        p1 = Post(titulo="Meu primeiro post", conteudo="Conteúdo do post", autor_id=u1.id)
        p2 = Post(titulo="Receita de bolo", conteudo="Misture tudo e asse", autor_id=u2.id)
        session.add_all([p1, p2])
        session.commit()

        # Comentários
        com1 = Comentario(conteudo="Ótimo post!", autor_id=u2.id, post_id=p1.id)
        com2 = Comentario(conteudo="Amei essa receita!", autor_id=u1.id, post_id=p2.id)
        session.add_all([com1, com2])
        session.commit()

        # Curtidas
        curt1 = Curtida(usuario_id=u2.id, post_id=p1.id)
        curt2 = Curtida(usuario_id=u1.id, post_id=p2.id)
        session.add_all([curt1, curt2])
        session.commit()

        print("✅ Banco populado com sucesso!")

if __name__ == "__main__":
    popular()
