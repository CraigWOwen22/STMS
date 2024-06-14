import React, { useEffect, useState } from 'react';
import './CreateBookingModal.css';

const CreateBookingModal = ({ show, onClose, token}) => {
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

    useEffect(() => {
        const fetchSectionSeats = async () => {
            if (!date) return; // Don't fetch data if date is not set

            const formattedDate = new Date(date).toISOString().split('T')[0]; // Format date to yyyy-mm-dd

            try {
                const response = await fetch(`http://127.0.0.1:8000/bookings/getallsectionseats?dateData=${formattedDate}`);
                const data = await response.json();
                setOptions(data);

                // Fetch total seats from getAllSeats API
                const totalSeatsResponse = await fetch(`http://127.0.0.1:8000/bookings/getallseats?dateData=${formattedDate}`);
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

    useEffect(() => {
        const fetchPrices = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/theatre/getallprices`);
                const pricesData = await response.json();
                setPrices(pricesData);
            } catch (error) {
                console.error('Error fetching prices:', error);
            }
        };

        fetchPrices();
    }, []); // Fetch prices only once, when the component mounts

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

    useEffect(() => {
        if (section && selectedValue) {
            const selectedSectionPrice = prices.find(item => item.section === section);

            if (selectedSectionPrice) {
                const pricePerSeat = selectedSectionPrice.price;
                const seatQuantity = parseInt(selectedValue, 10); // Convert selectedValue to integer
                const totalPriceCalculation = pricePerSeat * seatQuantity;

                setTotalPrice(totalPriceCalculation);
            } else {
                setTotalPrice(null); // Handle case where section price is not found
            }
        } else {
            setTotalPrice(null); // Reset total price if section or selectedValue changes to empty or null
        }
    }, [section, selectedValue, prices]);

    if (!show) {
        return null;
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Convert selectedValue to integer
        const seatQuantity = parseInt(selectedValue, 10);

        // Find price per seat for the selected section
        const selectedSectionPrice = prices.find(item => item.section === section);
        if (!selectedSectionPrice) {
            console.error(`Price for section ${section} not found.`);
            return;
        }
        const pricePerSeat = selectedSectionPrice.price;

        // Calculate total price
        const totalPriceCalculation = pricePerSeat * seatQuantity;

        // Prepare payload for POST request
        const payload = {
            section: section,
            seats: seatQuantity,
            price: totalPriceCalculation,
            bookingDate: date
        };

        try {
            // Make POST request
            const response = await fetch('http://127.0.0.1:8000/bookings/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Booking created successfully:', data);
                // Handle success, maybe show a success message or redirect
            } else {
                console.error('Failed to create booking:', response.status);
                // Handle error, maybe show an error message
            }
        } catch (error) {
            console.error('Error creating booking:', error);
            // Handle error, maybe show an error message
        }

        // Close modal after submission
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
