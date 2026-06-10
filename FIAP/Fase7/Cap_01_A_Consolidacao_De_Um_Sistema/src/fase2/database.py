"""
Fase 2 — Banco de Dados Estruturado
Esquema relacional FarmTech em SQLite (adaptado do modelo Oracle da Fase 2).
CRUD completo para culturas, sensores, irrigação e colheitas.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

import sys
_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))
from src.config import DB_PATH


def conectar() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_schema() -> None:
    """Cria todas as tabelas do sistema FarmTech (MER/DER da Fase 2)."""
    ddl = """
    CREATE TABLE IF NOT EXISTS tbl_culturas (
        id_cultura    INTEGER PRIMARY KEY AUTOINCREMENT,
        nome          TEXT    NOT NULL,
        variedade     TEXT,
        area_ha       REAL    NOT NULL,
        data_plantio  TEXT    NOT NULL,
        ph_ideal_min  REAL    DEFAULT 5.5,
        ph_ideal_max  REAL    DEFAULT 7.5,
        umid_ideal_min REAL   DEFAULT 35.0,
        umid_ideal_max REAL   DEFAULT 65.0
    );

    CREATE TABLE IF NOT EXISTS tbl_sensores (
        id_leitura     INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cultura     INTEGER REFERENCES tbl_culturas(id_cultura),
        timestamp      TEXT    NOT NULL DEFAULT (datetime('now')),
        umidade_solo   REAL,
        ph             REAL,
        nitrogenio     INTEGER DEFAULT 0,
        fosforo        INTEGER DEFAULT 0,
        potassio       INTEGER DEFAULT 0,
        temperatura_c  REAL,
        prob_chuva     REAL    DEFAULT 0.0,
        chuva_3h_mm    REAL    DEFAULT 0.0,
        bloquear_irrig INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS tbl_irrigacao (
        id_evento      INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cultura     INTEGER REFERENCES tbl_culturas(id_cultura),
        timestamp      TEXT    NOT NULL DEFAULT (datetime('now')),
        duracao_min    REAL,
        volume_litros  REAL,
        motivo_ativacao TEXT,
        bomba_ligada   INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS tbl_colheitas (
        id_colheita      INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cultura       INTEGER REFERENCES tbl_culturas(id_cultura),
        data_colheita    TEXT    NOT NULL,
        producao_ton     REAL,
        perda_ton        REAL    DEFAULT 0,
        tipo_colheita    TEXT    DEFAULT 'mecanica',
        eficiencia_pct   REAL,
        classificacao    TEXT
    );
    """
    with conectar() as conn:
        conn.executescript(ddl)
    print(f"Schema FarmTech criado/verificado em: {DB_PATH}")


# ── CRUD: Culturas ────────────────────────────────────────────────────────────

def inserir_cultura(nome: str, variedade: str, area_ha: float,
                    data_plantio: str = None) -> int:
    data_plantio = data_plantio or datetime.now().strftime("%Y-%m-%d")
    with conectar() as conn:
        cur = conn.execute(
            "INSERT INTO tbl_culturas (nome, variedade, area_ha, data_plantio) VALUES (?,?,?,?)",
            (nome, variedade, area_ha, data_plantio),
        )
    return cur.lastrowid


def listar_culturas() -> list[dict]:
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM tbl_culturas ORDER BY id_cultura").fetchall()
    return [dict(r) for r in rows]


def atualizar_cultura(id_cultura: int, area_ha: float) -> None:
    with conectar() as conn:
        conn.execute(
            "UPDATE tbl_culturas SET area_ha=? WHERE id_cultura=?",
            (area_ha, id_cultura),
        )


def deletar_cultura(id_cultura: int) -> None:
    with conectar() as conn:
        conn.execute("DELETE FROM tbl_culturas WHERE id_cultura=?", (id_cultura,))


# ── CRUD: Sensores ────────────────────────────────────────────────────────────

def inserir_leitura(id_cultura: int, umidade: float, ph: float,
                    n: int, p: int, k: int, temp: float = None,
                    prob_chuva: float = 0.0, chuva_3h: float = 0.0,
                    bloquear: bool = False) -> int:
    with conectar() as conn:
        cur = conn.execute(
            """INSERT INTO tbl_sensores
               (id_cultura, umidade_solo, ph, nitrogenio, fosforo, potassio,
                temperatura_c, prob_chuva, chuva_3h_mm, bloquear_irrig)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (id_cultura, umidade, ph, n, p, k, temp, prob_chuva, chuva_3h, int(bloquear)),
        )
    return cur.lastrowid


def ultimas_leituras(id_cultura: int = None, limite: int = 50) -> list[dict]:
    sql = "SELECT * FROM tbl_sensores"
    params: list = []
    if id_cultura is not None:
        sql += " WHERE id_cultura=?"
        params.append(id_cultura)
    sql += " ORDER BY id_leitura DESC LIMIT ?"
    params.append(limite)
    with conectar() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


# ── CRUD: Irrigação ───────────────────────────────────────────────────────────

def registrar_irrigacao(id_cultura: int, duracao_min: float,
                        volume_litros: float, motivo: str) -> int:
    with conectar() as conn:
        cur = conn.execute(
            """INSERT INTO tbl_irrigacao
               (id_cultura, duracao_min, volume_litros, motivo_ativacao)
               VALUES (?,?,?,?)""",
            (id_cultura, duracao_min, volume_litros, motivo),
        )
    return cur.lastrowid


def historico_irrigacao(id_cultura: int = None, limite: int = 20) -> list[dict]:
    sql = "SELECT * FROM tbl_irrigacao"
    params: list = []
    if id_cultura is not None:
        sql += " WHERE id_cultura=?"
        params.append(id_cultura)
    sql += " ORDER BY id_evento DESC LIMIT ?"
    params.append(limite)
    with conectar() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


# ── CRUD: Colheitas ───────────────────────────────────────────────────────────

def registrar_colheita(id_cultura: int, data: str, producao_ton: float,
                       perda_ton: float = 0.0, tipo: str = "mecanica") -> int:
    eficiencia = round((1 - perda_ton / producao_ton) * 100, 2) if producao_ton > 0 else 0
    classificacao = (
        "Excelente" if eficiencia >= 90 else
        "Boa"       if eficiencia >= 75 else
        "Regular"   if eficiencia >= 55 else "Baixa"
    )
    with conectar() as conn:
        cur = conn.execute(
            """INSERT INTO tbl_colheitas
               (id_cultura, data_colheita, producao_ton, perda_ton,
                tipo_colheita, eficiencia_pct, classificacao)
               VALUES (?,?,?,?,?,?,?)""",
            (id_cultura, data, producao_ton, perda_ton, tipo, eficiencia, classificacao),
        )
    return cur.lastrowid


def listar_colheitas(id_cultura: int = None) -> list[dict]:
    sql = "SELECT * FROM tbl_colheitas"
    params: list = []
    if id_cultura is not None:
        sql += " WHERE id_cultura=?"
        params.append(id_cultura)
    sql += " ORDER BY data_colheita DESC"
    with conectar() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


# ── Inicialização ─────────────────────────────────────────────────────────────

def inicializar_db() -> None:
    """Cria o schema e insere cultura-padrão se o banco estiver vazio."""
    criar_schema()
    culturas = listar_culturas()
    if not culturas:
        inserir_cultura("Soja", "Convencional", 50.0, "2024-10-01")
        inserir_cultura("Milho", "Híbrido", 30.0, "2024-09-15")
        inserir_cultura("Café", "Arábica", 20.0, "2024-08-01")
        print("Culturas padrão inseridas.")


if __name__ == "__main__":
    inicializar_db()
    print("Culturas:", listar_culturas())
