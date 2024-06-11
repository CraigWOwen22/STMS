import React, { useEffect, useState } from 'react';
import './CreateBookingModal.css';

const CreateBookingModal = ({ show, onClose, onSubmit, userToken }) => {
    const [section, setSection] = useState('');
    const [date, setDate] = useState('');
    const [options, setOptions] = useState([{section: "A", seats: 29},{section: "B", seats: 19},{section: "C", seats:9} ])

// useEffect(() => {
//     // GET SECTIONS SEATS API
//     setOptions(response)
// },[])

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
                    {options.map((option) => (
                        <label>
                            <input type="radio" name="section" value={option.section} required onChange={(e) => setSection(e.target.value)} /> Section {option.section} - {option.seats} Seats Available
                        </label>
                    ))}
                    {/* <label>
                        <input type="radio" name="section" value="A" required onChange={(e) => setSection(e.target.value)} /> Section A - 33 Seats Available
                    </label> */}
<br />
                    <label for="date">Date:</label>
                    <input type="date" id="date" name="date" required onChange={(e) => setDate(e.target.value)} /><br />
                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
};

export default CreateBookingModal;
