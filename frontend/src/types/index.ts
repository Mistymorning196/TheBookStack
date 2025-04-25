export interface Reader {
    id: number;
    api: string;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: number;
    password: string;
    book_count: number;
    goal_one: number;
    goal_two: number;
    goal_three: number;
    goal_four: number;
    goal_five: number;
}

export interface Author {
    id: number;
    api: string;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: number;
    password: string;
    biography: string;
}

export interface Book {
    id: number;
    api: string;
    author: string;
    title: string;
    blurb: string;
    isbn: string;
    cover_image: string;
}


export interface Blog{
    id: number;
    api: string;
    title: string;
    post : string;
    author: string;
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
    author: string;
    title: string;
    cover_image: string;
}

export interface AuthorBook{
    id: number;
    api: string;
    user: number;
    book: number;
    author: string;
    title: string;
    cover_image: string;
}

export interface AuthorBlog{
    id: number;
    api: string;
    user: number;
    blog: number;
    author: string;
    title: string;
}

export interface ReaderGenre{
    id: number;
    api: string;
    user: number;
    genre: number;
    name: string;
    count: number;
}

export interface BookGenre{
    id: number;
    api: string;
    book: number;
    genre: number;
    name: string;
}

export interface Genre{
    id: number;
    api: string;
    type: string;
    description: string;
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

export interface Comment{
    id: number;
    api: string;
    blog: number;
    user: number;
    username: string;
    comment: string;
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

