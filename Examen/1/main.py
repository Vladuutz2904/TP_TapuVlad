from checker import (
    SITES,
    build_url,
    check_headers,
    check_site,
    is_https,
    retry_check,
    scan_sites,
    show_response,
)


if __name__ == "__main__":
    print("Partea 1, build_url:", build_url("example.com", "login"))
    print("Partea 1, build_url:", build_url("example.com", "/login"))
    print("Partea 1, is_https:", is_https(SITES[0]))
    print("Partea 1, is_https:", is_https(SITES[9]))

    print("Partea 2, show_response:")
    show_response(SITES[0])
    print("Partea 2, show_response:")
    show_response(SITES[9])

    print("Partea 3, check_site:", check_site(SITES[0]))
    print("Partea 3, check_site:", check_site(SITES[9]))

    print("Partea 4, scan_sites:")
    scan_sites()

    print("Partea 5, check_headers:", check_headers(SITES[10]))
    print("Partea 5, check_headers:", check_headers(SITES[0]))

    print("Partea 6, retry_check:", retry_check(SITES[3]))
    print("Partea 6, retry_check:", retry_check(SITES[6]))
    print("Partea 6, retry_check:", retry_check(SITES[7]))
    print("Partea 6, retry_check:", retry_check(SITES[9]))
