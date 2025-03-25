export interface Reader {
    id: number;
    api: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: number;
    password: string;
    book_count: number;
}

export interface Book{
    id: number;
    api: string;
    author: string;
    title: string;
    blurb : string;
    isbn: string;
}

export interface Friendship{
    id: number;
    api: string;
    user: number;
    friend: number;
    userUsername: string;
    friendUsername: string;
    accepted: boolean;
}

export interface UserBook{
    id: number;
    api: string;
    user: number;
    book: number;
    status: string;
}

export interface Review{
    id: number;
    api: string;
    book: number;
    user: number;
    title: string;
    username: string;
    rating: number;
    message: string;
}

export interface Message{
    id: number;
    api: string;
    user: number;
    friend: number;
    userUsername: string;
    friendUsername: string;
    message: string;
}

