export const UserMarkerLayout = ({ imageUrl = "/assets/user_default_icon.png" }: { imageUrl: string }) => {
	return (
		<div className='w-full aspect-square rounded-[50%] bg-white flex items-center justify-center border-2 border-[#ccc] shadow-lg'>
      <img
        src={imageUrl}
        alt="User"
        style={{
          width: 28,
          height: 28,
          borderRadius: '50%',
          objectFit: 'cover',
        }}
      />
      <span className='text-sm text-red-500 font-medium'>Nigger is pidor</span>
    </div>
	)
}