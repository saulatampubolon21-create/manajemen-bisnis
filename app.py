import streamlit as st
import pandas as pd
import os

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Manajer Bisnis Saya", layout="wide")

# 2. Fungsi untuk Mengelola Data (Disimpan di file CSV)
DB_FILE = "data_penjualan.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Tanggal", "Produk", "Modal", "Harga Jual", "Untung"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# 3. Judul Aplikasi
st.title("📈 Dashboard Bisnis Sampingan")
st.write("Kelola pendapatan dan modal kamu secara otomatis.")

# 4. Input Data (Sidebar)
with st.sidebar:
    st.header("Tambah Penjualan")
    with st.form("input_form", clear_on_submit=True):
        tgl = st.date_input("Tanggal")
        nama = st.text_input("Nama Produk")
        modal = st.number_input("Modal per Item (Rp)", min_value=0)
        harga = st.number_input("Harga Jual (Rp)", min_value=0)
        
        submit = st.form_submit_button("Simpan Penjualan")
        
        if submit and nama:
            untung = harga - modal
            df = load_data()
            new_row = pd.DataFrame([[tgl, nama, modal, harga, untung]], 
                                   columns=["Tanggal", "Produk", "Modal", "Harga Jual", "Untung"])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success(f"Berhasil menyimpan {nama}!")

# 5. Tampilan Dashboard
df = load_data()

if not df.empty:
    # Baris Angka Utama (Metrics)
    total_omzet = df["Harga Jual"].sum()
    total_modal = df["Modal"].sum()
    total_untung = df["Untung"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Omzet", f"Rp {total_omzet:,}")
    col2.metric("Total Modal", f"Rp {total_modal:,}")
    col3.metric("Untung Bersih", f"Rp {total_untung:,}")
    
    st.divider()
    
    # Tabel Data
    st.subheader("Riwayat Penjualan")
    st.dataframe(df, use_container_width=True)
    
    # Tombol Reset (Hanya jika ingin hapus semua data)
    if st.button("Hapus Semua Data"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
else:
    st.info("Belum ada data. Silakan masukkan penjualan pertama kamu di sidebar sebelah kiri!")
