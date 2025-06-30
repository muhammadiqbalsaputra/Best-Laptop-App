from flask import (
    Flask, render_template, request, redirect, url_for, flash
)
from DBConnection import db_cursor
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "spk_secret_key"

# --------------------------------------------------
#  UTIL
# --------------------------------------------------

def to_float(val, default=1.0):
    """Konversi Decimal/None → float agar pow() tidak error."""
    if val is None:
        return float(default)
    if isinstance(val, Decimal):
        return float(val)
    return float(val)

# --------------------------------------------------
#  DASHBOARD
# --------------------------------------------------
@app.route("/")
def dashboard():
    with db_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM alternatif")
        total_alt = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) AS n FROM kriteria")
        total_krit = cur.fetchone()["n"]
    return render_template("dashboard.html", total_alt=total_alt, total_krit=total_krit)

# --------------------------------------------------
#  K R I T E R I A  (CRUD)
# --------------------------------------------------
@app.route("/kriteria", methods=["GET", "POST"])
def kriteria():
    if request.method == "POST":
        nama  = request.form.get("nama")
        bobot = request.form.get("bobot", type=int)
        if not nama or not (1 <= bobot <= 5):
            flash("Nama & bobot 1‑5 wajib diisi", "danger")
        else:
            try:
                with db_cursor() as cur:
                    cur.execute("INSERT INTO kriteria (nama, bobot) VALUES (%s, %s)", (nama, bobot))
                flash("Kriteria ditambahkan", "success")
            except Exception as e:
                flash(f"Gagal: {e}", "danger")
        return redirect(url_for("kriteria"))

    with db_cursor() as cur:
        cur.execute("SELECT * FROM kriteria ORDER BY id")
        kriterias = cur.fetchall()
    return render_template("kriteria.html", kriterias=kriterias)

@app.route("/kriteria/delete/<int:id>")
def del_kriteria(id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM kriteria WHERE id=%s", (id,))
    flash("Kriteria dihapus", "info")
    return redirect(url_for("kriteria"))

# --------------------------------------------------
#  EDIT   K R I T E R I A  (GET form • POST update)
# --------------------------------------------------
@app.route("/kriteria/edit/<int:id>", methods=["GET", "POST"])
def edit_kriteria(id):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM kriteria WHERE id=%s", (id,))
        k = cur.fetchone()
        if not k:
            flash("Kriteria tidak ditemukan", "danger")
            return redirect(url_for("kriteria"))

        if request.method == "POST":
            nama_baru  = request.form.get("nama")
            bobot_baru = request.form.get("bobot", type=int)
            if not nama_baru or not (1 <= bobot_baru <= 5):
                flash("Nama & bobot 1‑5 wajib diisi", "danger")
            else:
                cur.execute(
                    "UPDATE kriteria SET nama=%s, bobot=%s WHERE id=%s",
                    (nama_baru, bobot_baru, id)
                )
                flash("Kriteria diperbarui", "success")
                return redirect(url_for("kriteria"))

    # GET – tampilkan form
    return render_template("kriteria_edit.html", k=k)

# Kriteria ADD
@app.route("/kriteria/add", methods=["GET", "POST"])
def add_kriteria():
    if request.method == "POST":
        nama  = request.form.get("nama")
        bobot = request.form.get("bobot", type=int)
        if not nama or not (1 <= bobot <= 5):
            flash("Nama dan bobot (1–5) wajib diisi", "danger")
        else:
            with db_cursor() as cur:
                cur.execute("INSERT INTO kriteria (nama, bobot) VALUES (%s, %s)", (nama, bobot))
            flash("Kriteria ditambahkan", "success")
            return redirect(url_for("kriteria"))
    return render_template("kriteria_add.html")



# --------------------------------------------------
#  A L T E R N A T I F  (CRUD + Tampilan skor)
# --------------------------------------------------
@app.route("/alternatif", methods=["GET", "POST"])
def alternatif():
    if request.method == "POST":
        nama = request.form.get("nama")
        if not nama:
            flash("Nama laptop wajib diisi", "danger")
        else:
            try:
                with db_cursor() as cur:
                    cur.execute("INSERT INTO alternatif (nama) VALUES (%s)", (nama,))
                flash("Alternatif ditambahkan", "success")
            except Exception as e:
                flash(f"Gagal: {e}", "danger")
        return redirect(url_for("alternatif"))

    with db_cursor() as cur:
        cur.execute("SELECT * FROM alternatif ORDER BY id")
        alternatifs = cur.fetchall()
        cur.execute("SELECT * FROM kriteria ORDER BY id")
        kriterias = cur.fetchall()
        cur.execute("SELECT alternatif_id, kriteria_id, nilai FROM skor")
        nilai_map = {f"{r['alternatif_id']}-{r['kriteria_id']}": to_float(r['nilai']) for r in cur.fetchall()}
    return render_template("alternatif.html", alternatifs=alternatifs, kriterias=kriterias, nilai=nilai_map)

@app.route("/alternatif/delete/<int:id>")
def del_alternatif(id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM alternatif WHERE id=%s", (id,))
    flash("Alternatif dihapus", "info")
    return redirect(url_for("alternatif"))

# Hapus skor tunggal
@app.route("/alternatif/<int:alt_id>/skor/delete/<int:krit_id>")
def del_skor(alt_id, krit_id):
    with db_cursor() as cur:
        cur.execute("DELETE FROM skor WHERE alternatif_id=%s AND kriteria_id=%s", (alt_id, krit_id))
    flash("Skor dihapus", "info")
    return redirect(url_for("alternatif"))

# Form isi / edit skor untuk satu alternatif
@app.route("/alternatif/<int:alt_id>/skor", methods=["GET", "POST"])
def skor_alt(alt_id):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM alternatif WHERE id=%s", (alt_id,))
        alt = cur.fetchone()
        if not alt:
            flash("Alternatif tidak ditemukan", "danger")
            return redirect(url_for("alternatif"))
        cur.execute("SELECT * FROM kriteria ORDER BY id")
        kriterias = cur.fetchall()

        if request.method == "POST":
            for k in kriterias:
                nilai = request.form.get(f"k_{k['id']}", type=float)
                if nilai is None:
                    continue
                cur.execute(
                    """
                    INSERT INTO skor (alternatif_id, kriteria_id, nilai)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE nilai = VALUES(nilai)
                    """,
                    (alt_id, k['id'], nilai)
                )
            flash("Skor tersimpan", "success")
            return redirect(url_for("alternatif"))

        cur.execute("SELECT kriteria_id, nilai FROM skor WHERE alternatif_id=%s", (alt_id,))
        existing = {row['kriteria_id']: to_float(row['nilai']) for row in cur.fetchall()}

    return render_template("skor.html", alt=alt, kriterias=kriterias, existing=existing)

# --------------------------------------------------
#  EDIT ALTERNATIF (GET form • POST simpan)
# --------------------------------------------------
@app.route("/alternatif/edit/<int:id>", methods=["GET", "POST"])
def edit_alternatif(id):
    with db_cursor() as cur:
        # ambil data altenatif
        cur.execute("SELECT * FROM alternatif WHERE id=%s", (id,))
        alt = cur.fetchone()
        if not alt:
            flash("Alternatif tidak ditemukan", "danger")
            return redirect(url_for("alternatif"))

        if request.method == "POST":
            nama_baru = request.form.get("nama")
            if not nama_baru:
                flash("Nama tidak boleh kosong", "danger")
            else:
                cur.execute(
                    "UPDATE alternatif SET nama=%s WHERE id=%s",
                    (nama_baru, id),
                )
                flash("Alternatif diperbarui", "success")
                return redirect(url_for("alternatif"))

    # GET render form
    return render_template("alternatif_edit.html", alt=alt)

# --------------------------------------------------
#  TAMBAH ALTERNATIF  +  SKOR SEKALIGUS
# --------------------------------------------------
@app.route("/alternatif/add", methods=["GET", "POST"])
def add_alternatif():
    with db_cursor() as cur:
        # Ambil semua kriteria (dipakai GET & POST)
        cur.execute("SELECT * FROM kriteria ORDER BY id")
        kriterias = cur.fetchall()

        if request.method == "POST":
            nama = request.form.get("nama")
            if not nama:
                flash("Nama laptop wajib diisi", "danger")
                return redirect(url_for("add_alternatif"))

            try:
                # 1. Simpan alternatif
                cur.execute("INSERT INTO alternatif (nama) VALUES (%s)", (nama,))
                alt_id = cur.lastrowid

                # 2. Simpan skor per‑kriteria
                for k in kriterias:
                    nilai = request.form.get(f"k_{k['id']}", type=float)
                    if nilai is None:
                        continue
                    cur.execute(
                        """
                        INSERT INTO skor (alternatif_id, kriteria_id, nilai)
                        VALUES (%s, %s, %s)
                        """,
                        (alt_id, k['id'], nilai)
                    )

                flash("Alternatif & skor ditambahkan ✔", "success")
                return redirect(url_for("alternatif"))

            except Exception as e:
                flash(f"Gagal menambah alternatif: {e}", "danger")
                return redirect(url_for("add_alternatif"))

    # GET – tampilkan form
    return render_template("alternatif_add.html", kriterias=kriterias)

# --------------------------------------------------
#  R A N K I N G  (Weighted Product)
# --------------------------------------------------
@app.route("/rangking")
def rangking():
    with db_cursor() as cur:
        cur.execute("SELECT * FROM kriteria")
        kriterias = cur.fetchall()
        cur.execute("SELECT * FROM alternatif")
        alternatifs = cur.fetchall()

        total_bobot = sum(k['bobot'] for k in kriterias) or 1
        w = {k['id']: k['bobot'] / total_bobot for k in kriterias}

        hasil = []
        for alt in alternatifs:
            cur.execute("SELECT kriteria_id, nilai FROM skor WHERE alternatif_id=%s", (alt['id'],))
            skor_map = {row['kriteria_id']: to_float(row['nilai']) for row in cur.fetchall()}
            wp = 1.0
            for k in kriterias:
                v = skor_map.get(k['id'])
                if v is None:
                    continue  # atau v = 1.0 jika ingin default
                wp *= pow(v, w[k['id']])
            hasil.append({'nama': alt['nama'], 'wp': wp})

        total_wp = sum(h['wp'] for h in hasil) or 1.0
        for h in hasil:
            h['v'] = round(h['wp'] / total_wp, 6)

        hasil.sort(key=lambda x: x['v'], reverse=True)
        juara = hasil[0]['nama'] if hasil else '—'

    return render_template("rangking.html", hasil=hasil, juara=juara)

# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
