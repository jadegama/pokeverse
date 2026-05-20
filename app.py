import streamlit as st
import requests
import random
from PIL import Image
from PIL import ImageEnhance
from io import BytesIO
import base64

cores_tipos = {
    "fire": "#F08030",
    "water": "#6890F0",
    "grass": "#78C850",
    "electric": "#F8D030",
    "psychic": "#F85888",
    "ice": "#98D8D8",
    "dragon": "#7038F8",
    "dark": "#705848",
    "fairy": "#EE99AC",
    "normal": "#A8A878",
    "fighting": "#C03028",
    "flying": "#A890F0",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "rock": "#B8A038",
    "bug": "#A8B820",
    "ghost": "#705898",
    "steel": "#B8B8D0"
}

st.set_page_config(
    page_title="Pokédex Inteligente",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3 {
    color: #facc15;
    text-align: center;
}

p, label, div {
    color: white !important;
}

img {
    background: transparent !important;
}

.stTextInput input {
    background-color: #1e293b;
    color: white !important;
    border-radius: 15px;
    border: 2px solid #facc15;
    padding: 15px;
    font-size: 18px;
}

.stTextInput input::placeholder {
    color: #cbd5e1;
}

.stButton button {
    width: 100%;
    background-color: #facc15;
    color: black;
    border-radius: 15px;
    font-weight: bold;
    font-size: 18px;
    padding: 12px;
    border: none;
    transition: 0.3s;
}

.stButton button:hover {
    background-color: #fde047;
    color: black;
    transform: scale(1.02);
}

.stProgress > div > div > div > div {
    background-color: #facc15;
}

[data-testid="InputInstructions"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

def mostrar_imagem(url, largura=250):
    st.markdown(f"""
    <div style="text-align:center;">
        <img src="{url}" width="{largura}" style="object-fit:contain;">
    </div>
    """, unsafe_allow_html=True)

def mostrar_sombra(url, largura=250):
    st.markdown(f"""
    <div style="text-align:center;">
        <img src="{url}" width="{largura}" style="object-fit:contain; filter: brightness(0);">
    </div>
    """, unsafe_allow_html=True)

if "nome_jogador" not in st.session_state:
    st.session_state.nome_jogador = ""

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "nivel" not in st.session_state:
    st.session_state.nivel = 1

if st.session_state.nome_jogador == "":

    st.title("🎮 Bem-vindo ao PokeVerse!")

    st.markdown("""
    <div style="text-align:center; font-size:22px; margin-bottom:30px;">
    Digite seu nome para começar sua jornada Pokémon!
    </div>
    """, unsafe_allow_html=True)

    nome = st.text_input("", placeholder="Digite seu nome...")

    if st.button("🚀 Começar Jornada"):
        if nome != "":
            st.session_state.nome_jogador = nome
            st.rerun()

else:

    st.title(f"⚡ {st.session_state.nome_jogador}, sua jornada no PokeVerse começou!")

    st.markdown(f"""
    <div style="text-align:center; font-size:22px; margin-bottom:20px;">
    Nível: {st.session_state.nivel} ⭐
    </div>
    """, unsafe_allow_html=True)

    st.progress(st.session_state.xp / 100)
    st.write(f"XP: {st.session_state.xp}/100")

    st.markdown("""
    <div style="text-align:center; font-size:22px; margin-bottom:20px;">
    Descubra informações incríveis sobre Pokémon!
    </div>
    """, unsafe_allow_html=True)

    def mostrar_tipos(tipos):

        tipos_html = ""

        for tipo in tipos:
            cor = cores_tipos.get(tipo, "#777")

            tipos_html += f"""
            <span style="
                background-color:{cor};
                padding:8px 16px;
                border-radius:20px;
                margin-right:8px;
                color:white;
                font-weight:bold;
                font-size:16px;
            ">
            {tipo.upper()}
            </span>
            """

        st.markdown(tipos_html, unsafe_allow_html=True)

    def buscar_evolucoes(data):

        evolucoes = []

        species_url = data["species"]["url"]
        species_response = requests.get(species_url)

        if species_response.status_code == 200:

            species_data = species_response.json()
            evolution_url = species_data["evolution_chain"]["url"]

            evolution_response = requests.get(evolution_url)

            if evolution_response.status_code == 200:

                evolution_data = evolution_response.json()

                def percorrer_evolucao(chain):

                    nome = chain["species"]["name"].title()
                    url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"

                    response_pokemon = requests.get(url_pokemon)

                    imagem = None

                    if response_pokemon.status_code == 200:
                        data_pokemon = response_pokemon.json()
                        imagem = data_pokemon["sprites"]["other"]["official-artwork"]["front_default"]

                    evolucoes.append({
                        "nome": nome,
                        "imagem": imagem
                    })

                    for evolucao in chain["evolves_to"]:
                        percorrer_evolucao(evolucao)

                percorrer_evolucao(evolution_data["chain"])

        return evolucoes

    def buscar_pokemon(nome_ou_numero):

        url = f"https://pokeapi.co/api/v2/pokemon/{nome_ou_numero}"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            nome = data["name"].title()
            imagem = data["sprites"]["other"]["official-artwork"]["front_default"]

            tipos = [
                tipo["type"]["name"]
                for tipo in data["types"]
            ]

            altura = data["height"]
            peso = data["weight"]

            hp = data["stats"][0]["base_stat"]
            ataque_stat = data["stats"][1]["base_stat"]
            defesa = data["stats"][2]["base_stat"]

            ataques = []

            for move in data["moves"][:4]:
                ataques.append(move["move"]["name"].title())

            evolucoes = buscar_evolucoes(data)

            st.divider()

            mostrar_imagem(imagem, 300)

            st.markdown(f"# {nome}")

            mostrar_tipos(tipos)

            st.write(f"📏 Altura: {altura}")
            st.write(f"⚖️ Peso: {peso}")

            st.subheader("⚔️ Poderes")

            for atk in ataques:
                st.markdown(f"""
                <div style="
                    background-color:#1e293b;
                    padding:10px;
                    border-radius:12px;
                    margin-bottom:10px;
                    border:1px solid #facc15;
                    text-align:center;
                    font-weight:bold;
                ">
                    ⚡ {atk}
                </div>
                """, unsafe_allow_html=True)

            st.subheader("🧬 Evolução")

            if len(evolucoes) > 1:

                for i, evo in enumerate(evolucoes):

                    imagem_evo = evo["imagem"]
                    nome_evo = evo["nome"]

                    st.markdown(
    f"<div style='display:flex; align-items:center; justify-content:center; gap:20px; margin:15px auto; background-color:#1e293b; padding:15px; border-radius:18px; border:1px solid #334155; max-width:420px;'>"
    f"<img src='{imagem_evo}' style='width:95px; height:95px; object-fit:contain; background:transparent;'>"
    f"<span style='font-size:24px; font-weight:bold; color:white; white-space:nowrap;'>{nome_evo}</span>"
    f"</div>",
                    unsafe_allow_html=True
)

                    if i < len(evolucoes) - 1:

                        st.markdown("""
                        <div style="
                            text-align:center;
                            font-size:42px;
                            color:#facc15;
                            font-weight:bold;
                            margin:0;
                            line-height:1;
                        ">
                            ↓
                        </div>
                        """, unsafe_allow_html=True)

            else:

                st.info("✨ Este Pokémon não possui evolução.")

            st.subheader("📊 Estatísticas")

            st.write(f"❤️ HP: {hp}")
            st.progress(hp / 200)

            st.write(f"⚔️ Ataque: {ataque_stat}")
            st.progress(ataque_stat / 200)

            st.write(f"🛡️ Defesa: {defesa}")
            st.progress(defesa / 200)

        else:
            st.error("❌ Pokémon não encontrado!")

    st.subheader("🌟 Pokémon do Dia")

    if "pokemon_dia" not in st.session_state:
        st.session_state.pokemon_dia = random.randint(1, 151)

    pokemon_dia = st.session_state.pokemon_dia

    response_dia = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_dia}")

    if response_dia.status_code == 200:

        data_dia = response_dia.json()

        nome_dia = data_dia["name"].title()
        imagem_dia = data_dia["sprites"]["other"]["official-artwork"]["front_default"]

        tipos_dia = [
            tipo["type"]["name"]
            for tipo in data_dia["types"]
        ]

        mostrar_imagem(imagem_dia, 250)

        st.markdown(f"## {nome_dia}")

        mostrar_tipos(tipos_dia)

    st.markdown("""
    <h1 style="text-align:center; color:#facc15; margin-top:20px;">
    🔎 Encontre seu Pokémon
    </h1>

    <p style="text-align:center; color:white; font-size:20px; margin-bottom:30px;">
    Digite o nome do Pokémon favorito abaixo
    </p>
    """, unsafe_allow_html=True)

    pokemon = st.text_input(
        "",
        placeholder="⚡ Ex: Pikachu, Charizard, Eevee..."
    )

    if st.button("⚡ Buscar Pokémon"):
        if pokemon:
            buscar_pokemon(pokemon.lower())

    st.divider()

    st.subheader("🎲 Surpresa Pokémon")

    st.write("Clique no botão e descubra um Pokémon aleatório!")

    if st.button("🎮 Sortear Pokémon Aleatório"):

        numero = random.randint(1, 151)

        buscar_pokemon(numero)

    st.divider()

    if "pokemon_misterio" not in st.session_state:
        st.session_state.pokemon_misterio = random.randint(1, 151)

    pokemon_misterio = st.session_state.pokemon_misterio

    response_misterio = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{pokemon_misterio}"
    )

    if response_misterio.status_code == 200:

        data_misterio = response_misterio.json()

        nome_misterio = data_misterio["name"].title()

        imagem_misterio = data_misterio["sprites"]["other"]["official-artwork"]["front_default"]

        st.markdown("""
        <h2 style="text-align:center; color:white; margin-top:20px;">
        ❓ Quem é esse Pokémon?
        </h2>
        """, unsafe_allow_html=True)

        mostrar_sombra(imagem_misterio, 250)

        st.markdown("""
        <p style="text-align:center; font-size:18px; margin-top:10px;">
        Escolha o Pokémon correto:
        </p>
        """, unsafe_allow_html=True)

        if "opcoes_quiz" not in st.session_state:

            opcoes = [nome_misterio]

            while len(opcoes) < 4:

                numero_fake = random.randint(1, 151)

                response_fake = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{numero_fake}"
                )

                if response_fake.status_code == 200:

                    fake_nome = response_fake.json()["name"].title()

                    if fake_nome not in opcoes:
                        opcoes.append(fake_nome)

            random.shuffle(opcoes)

            st.session_state.opcoes_quiz = opcoes

        resposta = st.radio(
            "Escolha o Pokémon:",
            st.session_state.opcoes_quiz
        )

        if st.button("🎉 Revelar Pokémon"):

            mostrar_imagem(imagem_misterio, 250)

            st.success(f"É o {nome_misterio}!")

            if resposta == nome_misterio:

                st.balloons()

                st.success("🎯 Você acertou!")

                st.session_state.xp += 20

                if st.session_state.xp >= 100:

                    st.session_state.nivel += 1

                    st.session_state.xp = 0

                    st.balloons()

                    st.success("⬆️ Você subiu de nível!")

            else:
                st.error("❌ Você errou!")

        if st.button("🔄 Novo Pokémon"):

            st.session_state.pokemon_misterio = random.randint(1, 151)

            if "opcoes_quiz" in st.session_state:
                del st.session_state.opcoes_quiz

            st.rerun()