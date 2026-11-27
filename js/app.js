// Royal Safe Drive - Ultra Luxury Interactive Web App
document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Drawer
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileNav = document.getElementById('mobileNav');
  const mobileNavClose = document.getElementById('mobileNavClose');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

  if (mobileMenuBtn && mobileNav) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileNav.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      document.body.classList.add('menu-open');
    });
  }

  if (mobileNavClose && mobileNav) {
    mobileNavClose.addEventListener('click', () => {
      mobileNav.classList.add('hidden');
      document.body.style.overflow = 'auto';
      document.body.classList.remove('menu-open');
    });
  }

  mobileNavLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (mobileNav) {
        mobileNav.classList.add('hidden');
        document.body.style.overflow = 'auto';
        document.body.classList.remove('menu-open');
      }
    });
  });

  // Fare Estimator Elements
  const serviceTypeSelect = document.getElementById('calcServiceType');
  const pickupSelect = document.getElementById('calcPickup');
  const dropoffSelect = document.getElementById('calcDropoff');
  const hoursInput = document.getElementById('calcHours');
  const hoursContainer = document.getElementById('hoursContainer');
  const carTypeInput = document.getElementById('calcCar');
  const bookingTimeInput = document.getElementById('calcTime');
  const asapBtn = document.getElementById('btnAsap');
  const estimatedFareDisplay = document.getElementById('calcEstimatedFare');
  const estimatedDurationDisplay = document.getElementById('calcEstimatedDuration');
  const whatsappBookingBtn = document.getElementById('btnWhatsappBooking');

  // Service Switcher Pills in Booking Card
  const servicePillBtns = document.querySelectorAll('.service-pill-btn');
  servicePillBtns.forEach(pill => {
    pill.addEventListener('click', () => {
      servicePillBtns.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const val = pill.getAttribute('data-service');
      if (serviceTypeSelect) {
        serviceTypeSelect.value = val;
        updateServiceForm();
      }
    });
  });

  // Vehicle Quick Chips
  const vehicleChips = document.querySelectorAll('.vehicle-chip');
  vehicleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      vehicleChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const carName = chip.getAttribute('data-car');
      if (carTypeInput) {
        carTypeInput.value = carName;
        calculateFare();
      }
    });
  });

  // Toggle hours container if hourly chauffeur is selected
  function updateServiceForm() {
    if (!serviceTypeSelect) return;
    const isHourly = serviceTypeSelect.value === 'hourly';
    if (hoursContainer) {
      if (isHourly) {
        hoursContainer.classList.remove('hidden');
      } else {
        hoursContainer.classList.add('hidden');
      }
    }
    // Update active state of pills to match select
    servicePillBtns.forEach(pill => {
      if (pill.getAttribute('data-service') === serviceTypeSelect.value) {
        pill.classList.add('active');
      } else {
        pill.classList.remove('active');
      }
    });
    calculateFare();
  }

  if (serviceTypeSelect) {
    serviceTypeSelect.addEventListener('change', updateServiceForm);
  }
  if (pickupSelect) {
    pickupSelect.addEventListener('change', calculateFare);
  }
  if (dropoffSelect) {
    dropoffSelect.addEventListener('change', calculateFare);
  }
  if (hoursInput) {
    hoursInput.addEventListener('input', calculateFare);
  }

  // Quick ASAP Button
  if (asapBtn && bookingTimeInput) {
    asapBtn.addEventListener('click', () => {
      bookingTimeInput.value = 'ASAP (Next 15-20 Mins)';
      asapBtn.classList.add('bg-red-600', 'text-white');
      asapBtn.classList.remove('bg-red-950/60', 'text-red-400');
      calculateFare();
    });
  }

  function calculateFare() {
    if (!serviceTypeSelect || !estimatedFareDisplay) return;

    const service = serviceTypeSelect.value;
    const pickup = pickupSelect ? pickupSelect.value : 'Business Bay (Ontario Tower)';
    const dropoff = dropoffSelect ? dropoffSelect.value : 'Downtown Dubai';
    const hours = hoursInput ? parseInt(hoursInput.value, 10) || 4 : 4;

    let baseFare = 80;
    let fareText = 'AED 80 - 100';
    let durationText = '~15-20 mins arrival';

    if (service === 'hourly') {
      const calcHours = Math.max(hours, 2);
      const hourlyRate = 45;
      baseFare = calcHours * hourlyRate;
      fareText = `AED ${baseFare}`;
      durationText = `${calcHours} Hours Standby (@ 45/hr)`;
    } else if (service === 'full_day') {
      fareText = 'AED 550';
      durationText = 'Full Day (10 Hours Standby)';
      baseFare = 550;
    } else if (service === 'after_party') {
      fareText = 'AED 120';
      durationText = 'VIP After-Party Safe Ride';
      baseFare = 120;
    } else if (service === 'monthly') {
      fareText = 'AED 6,500';
      durationText = 'Monthly Retainer (6 Days/Wk)';
      baseFare = 6500;
    } else if (service === 'airport') {
      fareText = 'AED 120 - 150';
      durationText = 'Terminal Meet & Greet Included';
      baseFare = 120;
    } else if (service === 'rta_passing') {
      fareText = 'AED 150';
      durationText = '+ Official RTA Testing Fees';
      baseFare = 150;
    } else if (service === 'inter_emirate' || dropoff.includes('Abu Dhabi') || dropoff.includes('Sharjah') || dropoff.includes('Ajman') || dropoff.includes('RAK') || dropoff.includes('Fujairah') || dropoff.includes('Al Ain') || dropoff.includes('Umm Al Quwain')) {
      if (dropoff.includes('Sharjah')) {
        fareText = 'AED 200';
        durationText = 'Dubai ⇄ Sharjah (~35 mins)';
        baseFare = 200;
      } else if (dropoff.includes('Ajman')) {
        fareText = 'AED 280';
        durationText = 'Dubai ⇄ Ajman (~45 mins)';
        baseFare = 280;
      } else if (dropoff.includes('Umm Al Quwain')) {
        fareText = 'AED 300';
        durationText = 'Dubai ⇄ UAQ (~55 mins)';
        baseFare = 300;
      } else if (dropoff.includes('Abu Dhabi')) {
        fareText = 'AED 400';
        durationText = 'Dubai ⇄ Abu Dhabi (~1h 15m)';
        baseFare = 400;
      } else if (dropoff.includes('Ras Al Khaimah') || dropoff.includes('RAK')) {
        fareText = 'AED 400';
        durationText = 'Dubai ⇄ RAK (~1h 15m)';
        baseFare = 400;
      } else if (dropoff.includes('Fujairah')) {
        fareText = 'AED 400';
        durationText = 'Dubai ⇄ Fujairah (~1h 20m)';
        baseFare = 400;
      } else if (dropoff.includes('Al Ain')) {
        fareText = 'AED 400';
        durationText = 'Dubai ⇄ Al Ain (~1h 25m)';
        baseFare = 400;
      } else {
        fareText = 'AED 350 - 400';
        durationText = 'Inter-Emirates Highway Trip';
        baseFare = 400;
      }
    } else {
      // Standard One Way Safe Driver in Dubai City
      if (pickup === dropoff) {
        fareText = 'AED 80';
        durationText = 'Short Intra-Area Trip';
        baseFare = 80;
      } else if (
        (pickup.includes('Marina') || pickup.includes('Palm')) &&
        (dropoff.includes('Deira') || dropoff.includes('Airport') || dropoff.includes('Mirdif'))
      ) {
        fareText = 'AED 120 - 140';
        durationText = '~30-35 mins across town';
        baseFare = 120;
      } else {
        fareText = 'AED 80 - 100';
        durationText = '~15-20 mins typical ride';
        baseFare = 90;
      }
    }

    estimatedFareDisplay.textContent = fareText;
    if (estimatedDurationDisplay) {
      estimatedDurationDisplay.textContent = durationText;
    }
    updateWhatsAppLink(fareText, durationText);
  }

  function updateWhatsAppLink(currentFare, durationText) {
    if (!whatsappBookingBtn) return;

    const serviceName = serviceTypeSelect ? serviceTypeSelect.options[serviceTypeSelect.selectedIndex].text : 'Safe Driver';
    const pickup = pickupSelect ? pickupSelect.value : 'Business Bay';
    const dropoff = dropoffSelect ? dropoffSelect.value : 'Downtown Dubai';
    const timeVal = bookingTimeInput && bookingTimeInput.value ? bookingTimeInput.value : 'ASAP (Next 15-20 Mins)';
    const carVal = carTypeInput && carTypeInput.value ? carTypeInput.value : 'My Luxury Car';
    const hoursVal = hoursInput && serviceTypeSelect.value === 'hourly' ? `${hoursInput.value} Hours` : '';

    let text = `🏎️ *ROYAL SAFE DRIVE - DUBAI VIP BOOKING*\n`;
    text += `━━━━━━━━━━━━━━━━━━━━━\n`;
    text += `👑 *Service:* ${serviceName}\n`;
    text += `📍 *Pickup:* ${pickup}\n`;
    text += `🏁 *Destination:* ${dropoff}\n`;
    if (hoursVal) {
      text += `⏱️ *Standby:* ${hoursVal}\n`;
    }
    text += `⏰ *Time:* ${timeVal}\n`;
    text += `🚗 *Vehicle:* ${carVal}\n`;
    text += `💰 *Fare Quote:* ${currentFare} (${durationText})\n`;
    text += `━━━━━━━━━━━━━━━━━━━━━\n`;
    text += `Please dispatch an RTA-certified chauffeur from Ontario Tower, Business Bay HQ.`;

    const encoded = encodeURIComponent(text);
    whatsappBookingBtn.href = `https://wa.me/971503308757?text=${encoded}`;
  }

  // Inter-Emirate Quick Book Buttons
  const emirateButtons = document.querySelectorAll('.emirate-quick-book');
  emirateButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const destination = btn.getAttribute('data-destination');
      const fare = btn.getAttribute('data-fare');
      
      let msg = `🏎️ *ROYAL SAFE DRIVE - INTER-EMIRATE BOOKING*\n`;
      msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
      msg += `📍 *From:* Dubai\n`;
      msg += `🏁 *To:* ${destination}\n`;
      msg += `💰 *Fixed Rate:* ${fare}\n`;
      msg += `⏰ *Pickup Time:* ASAP / Scheduled\n`;
      msg += `━━━━━━━━━━━━━━━━━━━━━\n`;
      msg += `Please send driver details and confirm availability.`;
      
      const targetUrl = `https://wa.me/971503308757?text=${encodeURIComponent(msg)}`;
      window.open(targetUrl, '_blank');
    });
  });

  // Venue Hotspot Quick Selector
  const venueButtons = document.querySelectorAll('.venue-quick-book');
  venueButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const venueName = btn.getAttribute('data-venue');
      if (pickupSelect) {
        pickupSelect.value = venueName;
      }
      calculateFare();
      const calcElem = document.getElementById('booking-calculator');
      if (calcElem) {
        calcElem.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // FAQ Accordion
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');
    const icon = item.querySelector('.faq-icon');

    if (questionBtn && answer) {
      questionBtn.addEventListener('click', () => {
        const isOpen = !answer.classList.contains('hidden');
        faqItems.forEach(otherItem => {
          const otherAns = otherItem.querySelector('.faq-answer');
          const otherIcon = otherItem.querySelector('.faq-icon');
          if (otherAns) otherAns.classList.add('hidden');
          if (otherIcon) otherIcon.style.transform = 'rotate(0deg)';
        });

        if (!isOpen) {
          answer.classList.remove('hidden');
          if (icon) icon.style.transform = 'rotate(180deg)';
        }
      });
    }
  });

  // Quick Pickup Location Chips inside Calculator
  const quickPickupBtns = document.querySelectorAll('.quick-pickup-btn');
  quickPickupBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      quickPickupBtns.forEach(b => b.classList.remove('active', 'border-red-500', 'text-white'));
      btn.classList.add('active', 'border-red-500', 'text-white');
      const targetLoc = btn.getAttribute('data-pickup');
      if (pickupSelect && targetLoc) {
        pickupSelect.value = targetLoc;
        calculateFare();
      }
    });
  });

  // Live Driver Simulation Counter & Notification Ticker
  const liveCountElem = document.getElementById('liveDriverCount');
  if (liveCountElem) {
    const count = 18 + Math.floor(Math.random() * 6);
    liveCountElem.textContent = `${count} Chauffeurs Online`;
  }

  // Initial Calculation
  calculateFare();
});
