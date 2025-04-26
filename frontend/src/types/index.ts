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

    [key: string]: any;
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

    [key: string]: any;
}

export interface Book {
    id: number;
    api: string;
    author: string;
    title: string;
    blurb: string;
    isbn: string;
    cover_image: string;

    [key: string]: any;
}


export interface Blog{
    id: number;
    api: string;
    title: string;
    post : string;
    author: string;

    [key: string]: any;
}

export interface Group{
    id: number;
    api: string;
    name: string;

    [key: string]: any;
}

export interface Friendship{
    id: number;
    api: string;
    user: number;
    friend: number;
    userUsername: string;
    friendUsername: string;
    accepted: boolean;

    [key: string]: any;
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

    [key: string]: any;
}

export interface AuthorBook{
    id: number;
    api: string;
    user: number;
    book: number;
    author: string;
    title: string;
    cover_image: string;

    [key: string]: any;
}

export interface AuthorBlog{
    id: number;
    api: string;
    user: number;
    blog: number;
    author: string;
    title: string;

    [key: string]: any;
}

export interface ReaderGenre{
    id: number;
    api: string;
    user: number;
    genre: number;
    name: string;
    count: number;

    [key: string]: any;
}

export interface BookGenre{
    id: number;
    api: string;
    book: number;
    genre: number;
    name: string;

    [key: string]: any;
}

export interface Genre{
    id: number;
    api: string;
    type: string;
    description: string;

    [key: string]: any;
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

    [key: string]: any;
}

export interface Comment{
    id: number;
    api: string;
    blog_id: number;
    user_id: number;
    username: string;
    comment: string;

    [key: string]: any;
}

export interface Discussion{
    id: number;
    api: string;
    group_id: number;
    user_id: number;
    username: string;
    discussion: string;

    [key: string]: any;
}

export interface Message{
    id: number;
    api: string;
    user: number;
    friend: number;
    userUsername: string;
    friendUsername: string;
    message: string;

    [key: string]: any;
}

