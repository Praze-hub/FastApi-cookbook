from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from src.books.models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True #Helps with tracing every transaction that occurs
)
)


async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book
        # statement = text("SELECT 'hello';")
        
        # result = await conn.execute(statement)
        
        # print(result.all())
        await conn.run_sync(SQLModel.metadata.create_all)
        
async def get_session() -> AsyncSession: # type: ignore
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
        
    )
    
    async with Session() as session:
        yield session
        
        