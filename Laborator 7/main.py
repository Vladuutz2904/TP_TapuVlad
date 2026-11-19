from httptools import PATHS, report


def main():
    results = []
    for path in PATHS:
        info = report(path)
        info["path"] = path
        results.append(info)


    ok = [x for x in results if x["status"] == 200]
    ok.sort(key=lambda x: x["seconds"], reverse=True)
    for x in ok:
        print(f"{x['path']} -> {x['status']}, {x['seconds']:.2f} secunde")

    # 3. câte au reușit și câte au eșuat
    print(f"Reușite: {len(ok)} | Eșuate: {len(results) - len(ok)}")


if __name__ == "__main__":
    main()