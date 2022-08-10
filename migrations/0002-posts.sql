CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    content VARCHAR(5000) NOT NULL,
    image VARCHAR(250),
    preview_image VARCHAR(250),
    views INT DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED
);