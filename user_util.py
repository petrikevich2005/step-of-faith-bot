# user utils


# select username from text for ban/unban 
def select_username_from_text(text: str) -> str:
    username = []

    if len(text) > 0:
        for i in text:
            if i != " ":
                username.append(i)
            else:
                break

        return "".join(username)
    else:
        return "none"
