import Header from "@components/ui/Header"

export default function MainLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Header />
			<main className='w-full min-h-screen flex flex-col'>
				{children}
			</main>
		</>
  );
}
