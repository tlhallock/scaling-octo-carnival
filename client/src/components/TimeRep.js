
const TimeRep = ({time}) => (
  <label>
    {new Date(time).toLocaleString()}
  </label>
);

export default TimeRep;
