import Header from "@components/ui/Header"

export default function MainLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Header />
			<main className='w-full flex flex-col items-center min-h-[90vh]'>
				{children}
			</main>
		</>
  );
}
