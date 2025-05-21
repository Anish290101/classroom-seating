// --- Initial Seating Data (Translated from Python) ---
const initialSeating = [
    [  // Row 1
        ["Riddhima", "Samishtha"],  // Seat 1
        ["Yashika", "Harshi"],      // Seat 2
        ["Aditri", "Nitika"],       // Seat 3
        ["Tanushka", "Nivedita"],   // Seat 4
        ["Anaisha", "Ishani"],      // Seat 5
        ["Avika", "Ayesha"],        // Seat 6
    ],
    [  // Row 2
        ["Aadya", "Anushree"],      // Seat 1
        ["Yashasvi", "Tanishee"],   // Seat 2
        ["Sanskriti", "Samriddhi"], // Seat 3
        ["Vedant", "Saad"],         // Seat 4
        ["Abhiraj", "Vipul"],       // Seat 5
        ["Shaurya", "Siddhart"],    // Seat 6
    ],
    [  // Row 3
        ["Dev", null],              // Seat 1 (single student, use null for Python's None)
        ["Avyukta", "Raunak"],      // Seat 2
        ["Raghav", "Anish"],        // Seat 3
        ["Satvik", "Hemansh"],      // Seat 4
        ["Atharva", "Kunal"],       // Seat 5
        ["Himank", "Naitik"],       // Seat 6
    ],
    [  // Row 4
        ["Aryaman", null],          // Seat 1 (single student)
        ["Hammad", null],           // Seat 2 (single student)
        ["Affan", null],            // Seat 3 (single student)
        ["Aadhyan", "Aarav"],       // Seat 4
        ["Svakksh", "Tanay"],       // Seat 5
        ["Prakhyat", "Kartik"],     // Seat 6
    ],
];

// --- Core Logic Functions (Translated from Python to JavaScript) ---

function rotateSingleRowJS(rowData, rotationCount) {
    if (rowData.length === 0) {
        return [];
    }

    // Ensure rotationCount is within the bounds and positive for JS modulo behavior
    const effectiveRotation = (rotationCount % rowData.length + rowData.length) % rowData.length;

    // Perform the rotation: last 'effectiveRotation' elements moved to the front
    // Use slice and concat for array manipulation
    return rowData.slice(-effectiveRotation).concat(rowData.slice(0, -effectiveRotation));
}

function rotateSeatingRowWiseJS(seating, rotationCount) {
    // Use map to apply the rotation to each row independently
    return seating.map(row => rotateSingleRowJS(row, rotationCount));
}

function getRotationWeekFromDateJS(year, month, day) {
    // Month is 0-indexed in JavaScript's Date object (Jan=0, Dec=11)
    const startDate = new Date(2024, 0, 1); // January 1, 2024
    const targetDate = new Date(year, month - 1, day); // Adjust month input for JS

    // Check for invalid date (e.g., Feb 30)
    // Date.parse() returns NaN for invalid dates, then getTime() on NaN is also NaN
    if (isNaN(targetDate.getTime()) || targetDate.getFullYear() !== year || targetDate.getMonth() !== (month - 1) || targetDate.getDate() !== day) {
        return -1; // Indicate invalid date
    }

    // Calculate the difference in milliseconds
    // Note: Python's delta_days can be negative. JS Math.abs handles this for positive diff.
    const diffTime = targetDate.getTime() - startDate.getTime();

    // Convert milliseconds to days (1000 ms * 60 s * 60 min * 24 hrs)
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    // Integer division to get the number of full 7-day periods (weeks)
    const rotationWeek = Math.floor(diffDays / 7);

    return rotationWeek;
}

function validMonthJS(m) {
    return m >= 1 && m <= 12;
}

function validDayJS(d, m, y) {
    // JavaScript's Date object automatically handles invalid days,
    // e.g., new Date(2024, 1, 30) (Feb 30) will become March 1.
    // So, we create a date and check if it "rolled over".
    const date = new Date(y, m - 1, d); // Month is 0-indexed
    return date.getFullYear() === y && date.getMonth() === (m - 1) && date.getDate() === d;
}

// --- DOM Manipulation and Display Logic ---

function displaySeating() {
    // Get input elements and output areas
    const yearInput = document.getElementById('yearInput');
    const monthInput = document.getElementById('monthInput');
    const dayInput = document.getElementById('dayInput');
    const errorMessageElement = document.getElementById('errorMessage');
    const seatingOutputElement = document.getElementById('seatingOutput');

    // Clear previous messages and content
    errorMessageElement.textContent = '';
    seatingOutputElement.innerHTML = '';

    // Parse input values to integers
    const year = parseInt(yearInput.value);
    const month = parseInt(monthInput.value);
    const day = parseInt(dayInput.value);

    // Validate inputs
    if (isNaN(year) || isNaN(month) || isNaN(day)) {
        errorMessageElement.textContent = "Please enter valid numbers for year, month, and day.";
        return;
    }
    if (!validMonthJS(month)) {
        errorMessageElement.textContent = "Invalid month. Please input 1 to 12.";
        return;
    }
    if (!validDayJS(day, month, year)) {
        errorMessageElement.textContent = `Invalid day ${day} for month ${month} in year ${year}. Please re-enter.`;
        return;
    }

    // Calculate rotation week
    const rotationWeekCount = getRotationWeekFromDateJS(year, month, day);

    if (rotationWeekCount === -1) {
        errorMessageElement.textContent = "Error: Could not calculate rotation week for the given date. Please check input.";
        return;
    }

    // Perform seating rotation
    const rotatedSeating = rotateSeatingRowWiseJS(initialSeating, rotationWeekCount);

    // Build HTML for display
    let htmlContent = `<h2>Seating for ${month}/${day}/${year} (Rotation Week ${rotationWeekCount}):</h2>`;

    rotatedSeating.forEach((row, r_idx) => {
        htmlContent += `<div class="row-display"><h4>Row ${r_idx + 1}</h4><div class="seats-container">`;
        row.forEach((seat, s_idx) => {
            if (seat.length === 1 || (seat.length === 2 && seat[1] === null)) {
                htmlContent += `<span class="seat-item">Seat ${s_idx + 1}: ${seat[0]}</span>`;
            } else {
                htmlContent += `<span class="seat-item">Seat ${s_idx + 1}: ${seat[0]}, ${seat[1]}</span>`;
            }
        });
        htmlContent += `</div></div>`; // Close seats-container and row-display
    });

    // Update the output area
    seatingOutputElement.innerHTML = htmlContent;
}

// Set default values for inputs on page load
window.onload = function() {
    const today = new Date();
    document.getElementById('yearInput').value = today.getFullYear();
    document.getElementById('monthInput').value = today.getMonth() + 1; // Month is 0-indexed
    document.getElementById('dayInput').value = today.getDate();
    displaySeating(); // Display seating for today's date automatically
};