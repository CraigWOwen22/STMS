import React, { useEffect, useState } from 'react';
import './CreateBookingModal.css';

const CreateBookingModal = ({ show, onClose, onSubmit, userToken }) => {
    const [section, setSection] = useState('');
    const [date, setDate] = useState('');
    const [options, setOptions] = useState([]);
    const [totalSeats, setTotalSeats] = useState(null);
    console.log(date, section, totalSeats, )

    useEffect(() => {
        const fetchSectionSeats = async () => {
            if (!date) return; // Don't fetch data if date is not set

            const formattedDate = new Date(date).toISOString().split('T')[0]; // Format date to yyyy-mm-dd

            try {
                const response = await fetch(`http://127.0.0.1:8000/bookings/getallsectionseats?dateData=${formattedDate}`);
                const data = await response.json();
                setOptions(data);

                // Fetch total seats from getAllSeats API
                const totalSeatsResponse = await fetch(`http://127.0.0.1:8000/bookings/getAllSeats?dateData=${formattedDate}`);
                const totalSeatsData = await totalSeatsResponse.json();
                if (totalSeatsData && totalSeatsData.total) {
                    setTotalSeats(totalSeatsData.total);
                } else {
                    console.error('Invalid data format for total seats:', totalSeatsData);
                }
            } catch (error) {
                console.error('Error fetching section seats:', error);
            }
        };

        fetchSectionSeats();
    }, [date]);

    if (!show) {
        return null;
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        onSubmit({ section, date });
        onClose();
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <span className="close" onClick={onClose}>&times;</span>
                <h2>Create a New Booking</h2>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="date">Date:</label>
                    <input
                        type="date"
                        id="date"
                        name="date"
                        required
                        onChange={(e) => setDate(e.target.value)}
                    /><br />
                    {options.map((option) => (
                        <label key={option.key}>
                            <input
                                type="radio"
                                name="section"
                                value={option.key}
                                required
                                onChange={(e) => setSection(e.target.value)}
                            /> Section {option.key} - {option.value} Seats Available
                        </label>
                    ))}
                    <br />
                    {totalSeats !== null && (
                        <p>Total Seats Available: {totalSeats}</p>
                    )}
                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
};

export default CreateBookingModal;
