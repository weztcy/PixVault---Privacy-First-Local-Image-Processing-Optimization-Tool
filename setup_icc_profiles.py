"""Jalankan dari root PixVault: python setup_icc_profiles.py
Pasang profil asli: python setup_icc_profiles.py --source-dir /lokasi/profil
Folder sumber harus menggunakan nama yang tercantum dalam EXPECTED.
Tidak menggunakan internet. Memerlukan Pillow.
"""
import argparse
from pathlib import Path
import sys

from PIL import ImageCms

EXPECTED = {
    "AdobeRGB1998.icc": "RGB",
    "DisplayP3.icc": "RGB",
    "FOGRA39.icc": "CMYK",
    "Gray.icc": "GRAY",
    "sRGB.icc": "RGB",
}


def validate(path, expected):
    if not path.is_file() or path.stat().st_size < 128:
        raise ValueError("Berkas tidak ada, kosong, atau terlalu pendek untuk ICC")
    profile = ImageCms.getOpenProfile(str(path))
    space = str(profile.profile.xcolor_space).strip().upper()
    if space != expected:
        raise ValueError(f"Ruang warna {space!r}; diperlukan {expected}")
    return ImageCms.getProfileDescription(profile).strip()


def save_checked(data, destination, expected):
    temporary = destination.with_suffix(".icc.pending")
    if temporary.exists():
        raise ValueError(f"Berkas sementara sudah ada: {temporary}")
    try:
        temporary.write_bytes(data)
        validate(temporary, expected)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Siapkan profil ICC lokal PixVault")
    parser.add_argument("--source-dir", type=Path, help="Folder profil ICC asli")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    if not (root / "processing" / "colorspace.py").is_file():
        parser.error("Jalankan dari root PixVault atau berikan --project-root.")
    destination = root / "processing" / "profiles"
    destination.mkdir(parents=True, exist_ok=True)
    missing = []

    for name, space in EXPECTED.items():
        target = destination / name
        try:
            description = validate(target, space)
            print(f"DIPERTAHANKAN: {name} ({description})")
            continue
        except Exception:
            pass

        # Jangan menimpa profil tidak kosong yang mungkin perlu diperiksa.
        if target.exists() and (not target.is_file() or target.stat().st_size > 0):
            print(f"PERIKSA: {target} tidak valid; pindahkan secara manual dahulu.")
            missing.append(name)
            continue

        try:
            source = args.source_dir / name if args.source_dir else None
            if source is not None and source.is_file():
                validate(source, space)
                data = source.read_bytes()
            elif name == "sRGB.icc":
                data = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
            else:
                missing.append(name)
                print(f"DIPERLUKAN: profil ICC asli untuk {name}")
                continue
            save_checked(data, target, space)
            print(f"DISIMPAN: {target}")
        except Exception as exc:
            missing.append(name)
            print(f"GAGAL: {name}: {exc}")

    print("\nValidasi memeriksa keterbacaan ICC dan ruang warna, bukan keaslian profil.")
    print("Pastikan profil sumber benar, sesuai kondisi warna, dan berlisensi untuk penggunaan Anda.")
    print("Mengganti nama profil lain tidak menjadikannya Adobe RGB, Display P3, atau FOGRA39.")
    if missing:
        print("Belum lengkap: " + ", ".join(missing))
        return 1
    print("Semua berkas profil tersedia dan dapat dibaca.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
