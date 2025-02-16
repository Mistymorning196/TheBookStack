export interface User {
    id: number;
    api: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: number;
    password: string;
}

export interface Book{
    id: number;
    api: string;
    author: string;
    title: string;
    blurb : string;
    isbn: string;
}

