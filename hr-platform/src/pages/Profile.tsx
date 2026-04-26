interface User {
  name: string;
  phone: string;
  birthDate: string;
  citizenship: string;
}

export default function Profile({ user }: { user: User }) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.phone}</p>
      <p>{user.birthDate}</p>
      <p>{user.citizenship}</p>
    </div>
  );
}