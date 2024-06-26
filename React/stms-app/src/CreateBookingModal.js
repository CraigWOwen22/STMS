import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './CreateBookingModal.css';

const CreateBookingModal = ({ show, onClose, token }) => {
    const [section, setSection] = useState('');
    const [date, setDate] = useState('');
    const [options, setOptions] = useState([]);
    const [totalSeats, setTotalSeats] = useState(null);
    const [range, setRange] = useState([]);
    const [selectedValue, setSelectedValue] = useState('');
    const [prices, setPrices] = useState([
        { section: "A", price: 50 },
        { section: "B", price: 30 },
        { section: "C", price: 20 }
    ]);
    const [totalPrice, setTotalPrice] = useState(null);

    // Fetch all sections and set total seats in use state variables 
    useEffect(() => {
        const fetchSectionSeats = async () => {
            if (!date) return; 

            const formattedDate = new Date(date).toISOString().split('T')[0]; 

            try {
                const response = await axios.get(`http://127.0.0.1:8000/bookings/getallsectionseats?dateData=${formattedDate}`);
                setOptions(response.data);

                // Fetch total seats from getAllSeats API
                const totalSeatsResponse = await axios.get(`http://127.0.0.1:8000/bookings/getallseats?dateData=${formattedDate}`);
                if (totalSeatsResponse.data && totalSeatsResponse.data.total) {
                    setTotalSeats(totalSeatsResponse.data.total);
                } else {
                    console.error('Invalid data format for total seats:', totalSeatsResponse.data);
                }
            } catch (error) {
                console.error('Error fetching section seats:', error);
            }
        };

        fetchSectionSeats();
    }, [date, show]);

    // Fetch prices of sections
    useEffect(() => {
        const fetchPrices = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/theatre/getallprices');
                setPrices(response.data);
            } catch (error) {
                console.error('Error fetching prices:', error);
            }
        };

        fetchPrices();
    }, [show]); 

    // Fetch selected option and populate drop box accordingly
    useEffect(() => {
        if (section) {
            const selectedOption = options.find(option => option.key === section);
            if (selectedOption) {
                setRange([...Array(selectedOption.value + 1).keys()].slice(1));
            }
        } else {
            setRange([]);
        }
    }, [section, options]);

    // Work out total cost based on what is set in radio buttons and drop down box
    useEffect(() => {
        if (section && selectedValue) {
            const selectedSectionPrice = prices.find(item => item.section === section);

            if (selectedSectionPrice) {
                const pricePerSeat = selectedSectionPrice.price;
                const seatQuantity = parseInt(selectedValue, 10); // Convert selectedValue to integer
                const totalPriceCalculation = pricePerSeat * seatQuantity;

                setTotalPrice(totalPriceCalculation);
            } else {
                setTotalPrice(null);
            }
        } else {
            setTotalPrice(null); // Reset total price if section or selectedValue changes to empty or null
        }
    }, [section, selectedValue, prices]);


    // Submit the booking based on current use state variables 
    const handleSubmit = async (event) => {
        event.preventDefault();
    
        
        const payload = {
            section: section,
            seats: selectedValue,
            price: totalPrice,
            bookingDate: date
        };

        if (!section || !selectedValue || !totalPrice || !date) {
            console.error('Incorrect or empty fields! Please select correct fields and try again.');
            alert('Incorrect or empty fields! Please select correct fields and try again.');
            return; 
        }

        try {
            
            const response = await axios.post('http://127.0.0.1:8000/bookings/create', payload, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
        
            if (response.status === 200 || response.status === 201) {
                console.log('Booking created successfully:', response.data);
            } 
            else {
                console.error('Failed to create booking:', response.status);
            }
        } catch (error) {
            if (error.response && error.response.status === 409) {
                console.error('Not enough seats available.');
                alert('Not enough seats available. Please check seat availibility and try again.');
                return;
            } else {
                console.error('Error creating booking:', error);
            }
        }
        
        onClose();
    };

    if (!show) {
        return null;
    }

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
                        min={new Date().toISOString().split("T")[0]}
                        required
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                    /><br />
                    {options.map((option) => (
                        <label key={option.key}>
                            <input
                                type="radio"
                                name="section"
                                value={option.key}
                                required
                                checked={section === option.key}
                                onChange={(e) => setSection(e.target.value)}
                            /> Section {option.key} - {option.value} Seats Available
                        </label>
                    ))}
                    <br />
                    {range.length > 0 && (
                        <div>
                            <label htmlFor="range">Select Seat Quantity:</label>
                            <select
                                id="range"
                                name="range"
                                value={selectedValue}
                                onChange={(e) => setSelectedValue(e.target.value)}
                            >
                                <option value="">Select...</option>
                                {range.map((num) => (
                                    <option key={num} value={num}>{num}</option>
                                ))}
                            </select>
                        </div>
                    )}
                    {totalPrice !== null && (
                        <p>Total Price: £{totalPrice.toFixed(2)}</p>
                    )}
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
