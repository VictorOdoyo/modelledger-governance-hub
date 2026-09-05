
import httpx


def main() -> int:
    try:
        response = httpx.get("http://127.0.0.1:8088/health/ready", timeout=5)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"healthcheck failed: {exc}")
        return 1
    print("modelledger api ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
