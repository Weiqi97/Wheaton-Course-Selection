import * as utility from './utility.js'

/**
 * Convert time to proper format to display (Helper function).
 * @param {string} time - The time from the table that needs to be converted.
 * @returns {string} - Time in format of 'HH:MM:SS'.
 */
function timeConverter (time) {
  if (time.includes('A')) {
    if (time[2] === ':') {
      return `${time.slice(0, 5)}:00`
    } else {
      return `0${time.slice(0, 4)}:00`
    }
  } else {
    if (Number(time.slice(0, 2)) !== 12) {
      return `${Number(time.slice(0, 1)) + 12}${time.slice(1, 4)}:00`
    } else {
      return `${time.slice(0, 5)}:00`
    }
  }
}

/**
 * Convert day to proper format to display (Helper function).
 * @param {string} day - The day time that needs to be converted.
 * @returns {string} - The corresponding date.
 */
function dayConverter (day) {
  if (day === 'M') {
    return '2018-04-02T'
  } else if (day === 'T') {
    return '2018-04-03T'
  } else if (day === 'W') {
    return '2018-04-04T'
  } else if (day === 'R') {
    return '2018-04-05T'
  } else if (day === 'F') {
    return '2018-04-06T'
  }
}

/**
 * Check if there is an existing event that overlaps with the new event.
 * @param {Object} newEvent - The new event that needs to be added to calendar.
 * @returns {boolean} - If overlapping, return true, otherwise return false.
 */
function eventIsOverlap (newEvent) {
  const format = 'YYYY-MM-DD HH:mm:ss'
  const newEventStart = moment(newEvent.start).format(format)
  const newEventEnd = moment(newEvent.end).format(format)
  const allEvents = $('#calendar').fullCalendar('clientEvents')
  for (let event of allEvents) {
    if (moment(newEventStart).isBetween(event.start.format(format), event.end.format(format))) {
      return true
    } else if (moment(newEventEnd).isBetween(event.start.format(format), event.end.format(format))) {
      return true
    }
  }
  return false
}

/**
 * Alert user when events overlapping is detected.
 * @returns {void} - This function has no return.
 */
function overlapAlert () {
  $.confirm({
    type: 'red',
    icon: 'fas fa-exclamation-triangle',
    theme: 'modern',
    title: 'Cannot add this class.',
    content: 'There is an existing class in the calendar that is overlapping with this class.',
    buttons: {
      confirm: {
        text: 'Got it.',
        btnClass: 'btn-info'
      }
    }
  })
}

/**
 * This function creates the full calendar object.
 * @returns {void} - This function has no return.
 */
export function readyCalendar () {
  // Create the full calendar object.
  $('#calendar').fullCalendar({
    height: 800,
    header: { left: '', center: '', right: '' },
    editable: true, // Make the calendar editable.
    allDaySlot: false, // Hide "all day" at the top.
    defaultView: 'agendaWeek', // Display as weeks.
    columnFormat: 'dddd', // Display without dates.
    minTime: '8:00:00', // One day is from 8 to 22.
    maxTime: '23:00:00',
    hiddenDays: [0, 6], // Hide Saturday and Sunday.
    weekNumbers: false, // Hide week numbers.
    slotDuration: '00:30:00', // 30 minutes for each row.
    defaultDate: moment('2018-04-02'), // Set default date to be fixed.
    eventStartEditable: false, // Make existing even not editable.
    eventDurationEditable: false,

    // This part sets the delete events on click.
    eventRender (event, element) {
      element.find('.fc-bg').css('pointer-events', 'none')
      // Append the delete icon.
      element.append(
        `<div style='position: absolute; bottom: 1px; right: 2px'>
             <span id='deleteEvent'>
                 <i  class='fas fa-trash-alt fa-lg' style='color: orangered'></i>
             </span>
         </div>`
      )
      // Set the delete event trigger.
      element.find('#deleteEvent').click(function () {
        $('#calendar').fullCalendar('removeEvents', event._id)
      })
    }
  })
}

/**
 * Add class from data table to calendar.
 * @param {Object} event - The event object that was clicked.
 * @returns {void} - This function has no return.
 */
export function toCalendar (event) {
  // Get the row with the add button clicked.
  const clickedRow = $(event.currentTarget).closest('tr')
  // Get the data within the row.
  const rowData = $('#course-table').dataTable().fnGetData(clickedRow)
  // Unpack data from the row, we need title and time only.
  const courseTitle = rowData[4]
  const courseTime = rowData[5]

  // Check if the class has an assigned time.
  if (courseTime === 'TBA') {
    utility.classTimeTBAError()
  } else {
    // Split times. It is possible that one class has two different times.
    const timeList = courseTime.split('<br>')
    // Use a map function to fill all class times in the calendar.
    timeList.map(function (time) {
      const days = time.replace(/AM|PM|[0-9]|-|:|\s/g, '').split('')
      const startEndTime = time.replace(/[MTWRF]|\s/g, '').split('-')
      // Get all formatted events.
      const events = days.map(function (day) {
        return {
          id: courseTitle,
          title: courseTitle,
          start: dayConverter(day) + timeConverter(startEndTime[0]),
          end: dayConverter(day) + timeConverter(startEndTime[1]),
          allDay: false
        }
      })
      // Check if there is any overlapping.
      const eventsOverlap = events.map(function (event) {
        return eventIsOverlap(event)
      })
      console.log(eventsOverlap)
      // If no overlapping, render all events.
      if (eventsOverlap.indexOf(true) === -1) {
        events.map(function (event) {
          $('#calendar').fullCalendar('renderEvent', event, 'stick')
        })
      } else {
        // If overlapping detected, alert the user.
        overlapAlert()
      }
    })
  }
}
