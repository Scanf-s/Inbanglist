const StreamItem = ({ stream }) => {
  return (
    <div>
      <div>
        <img src={stream.thumbnail} alt={stream.title} />
      </div>
      <div>
        <h3>{stream.title}</h3>
        <span>{stream.channel_name}</span>
        <span> ⭐️ {stream.live_viewer}</span>
      </div>
    </div>
  )
}

export default StreamItem