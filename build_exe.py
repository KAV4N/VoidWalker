from PyInstaller.__main__ import run
import os
import sys
import shutil
from datetime import datetime

def create_build_dirs():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", f"build_{timestamp}")
    exe_dir = os.path.join(build_dir, "game")
    work_dir = os.path.join(build_dir, "work")
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(exe_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)
    return build_dir, exe_dir, work_dir

def copy_assets(exe_dir):
    assets_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    assets_dst = os.path.join(exe_dir, "assets")
    if os.path.exists(assets_src):
        print(f"Copying assets to {assets_dst}...")
        shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
    else:
        print("Warning: Assets directory not found!")

def clean_pyinstaller_artifacts():
    paths_to_clean = ['__pycache__', '*.spec']
    for pattern in paths_to_clean:
        files = [f for f in os.listdir('.') if f.endswith(pattern.replace('*', ''))]
        for f in files:
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
            except Exception as e:
                print(f"Warning: Could not remove {f}: {e}")

def build_executable():
    build_dir, exe_dir, work_dir = create_build_dirs()
    print(f"Created build directory: {build_dir}")
    project_root = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(project_root, "src", "main.py")
    src_path = os.path.join(project_root, "src")
    pyi_args = [
        main_file,
        "--onefile",
        "--noconsole",
        "--clean",
        "--name", "VoidWalker",
        "--distpath", exe_dir,
        "--workpath", work_dir,
        "--specpath", build_dir,
        "--paths", src_path,
        "--additional-hooks-dir", src_path,
    ]
    try:
        run(pyi_args)
        copy_assets(build_dir)
        clean_pyinstaller_artifacts()
        print(f"\nBuild completed successfully!")
        print(f"Build directory: {build_dir}")
        print("Contents:")
        print(f"  - game/")
        for item in os.listdir(exe_dir):
            print(f"    - {item}")
        print(f"  - work/")
        print(f"  - VoidWalker.spec")
    except Exception as e:
        print(f"Error during build: {e}")
        raise

if __name__ == "__main__":
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        os.system(f"{sys.executable} -m pip install pyinstaller")
    build_executable()
