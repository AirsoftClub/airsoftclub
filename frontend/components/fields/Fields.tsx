"use client";

import { useQuery } from "@tanstack/react-query";

export const Fields = (): JSX.Element => {
  const { data: posts } = useQuery(["posts"], async () => {
    const response = await fetch("https://jsonplaceholder.typicode.com/todos/");
    return response.json();
  });

  return (
    <div>
      <h1>Posts</h1>
      <ul>
        {posts?.map((post: any) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
};
