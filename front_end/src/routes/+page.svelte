<script>
	// @ts-nocheck

	import { onMount } from 'svelte';

	let currentPage = 1;
	let first_page = 1;
	let first_per_page = 1;
	let last_per_page = 15;
	let initial_count = 1;
	let itemsPerPage = 15;
	let pagenum = 0;
	let total_page;
	let page_count = 0;
	let searchData = [];
	let result = [];
	let uniqueResponseValues = {};
	let length = '';
	let bindStartDate = "";
	let bindEndDate = "";
	console.log(bindStartDate, 'bindStartDatebindStartDate');
	console.log(bindEndDate, 'bindEndDatebindEndDate');

	let isDropdownOpen = Array.from({ length: 17 }, () => false); // Array to store dropdown states

	function toggleDropdown(index) {
		isDropdownOpen[index] = !isDropdownOpen[index];
	}

	async function fetchData(currentPage) {
		try {
			const response = await fetch('http://localhost:5000/search', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					input_value: inputValue,
					page: currentPage,
					items_per_page: itemsPerPage,
					selected_checkboxes: selectedCheckboxes,
					bind_start_date: bindStartDate,
					bind_end_date: bindEndDate
				})
			})
			const data = await response.json();
			console.log(data, 'datadata');
			searchData = data.data;
			console.log(searchData, 'searchDatasearchData');
			length = data.total;
			result = data.result;
			total_page = Math.ceil(length / itemsPerPage);
			console.log(total_page, 'total_counttotal_count');
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

  async function fetchUniqueValues() {
		try {
      const uniquedata = await fetch('http://localhost:5000/unique_data', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					input_value: inputValue,
					distinct_key: distinctKey,
					search_params: searchParams,
					bind_start_date: bindStartDate,
					bind_end_date: bindEndDate
				})
			})
      const unique_data = await uniquedata.json();
      console.log(unique_data,"unique_data")
			uniqueResponseValues = unique_data.unique_values;
			console.log(uniqueResponseValues, 'uniqueResponseValues');
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	const handleSearch = () => {
		fetchUniqueValues()
	};

	let distinctKey = {
		msisdn: '',
		source_ip: '',
		source_port: '',
		destination_ip: '',
		destination_port: '',
		cell_id: '',
		company: '',
		domain: '',
		service: '',
		time: '',
		time_et: '',
		duration: '',
		uplink_vol: '',
		downlink_vol: '',
		com_type: '',
		roaming: '',
		provider: ''
	};
	let searchParams = {
		msisdn: '',
		source_ip: '',
		source_port: '',
		destination_ip: '',
		destination_port: '',
		cell_id: '',
		company: '',
		domain: '',
		service: '',
		time: '',
		time_et: '',
		duration: '',
		uplink_vol: '',
		downlink_vol: '',
		com_type: '',
		roaming: '',
		provider: ''
	};

	function convertToISO8601(textDate) {
		// Parse the input date string into a Date object
		const inputDate = new Date(textDate);

		// Format the Date object into the desired output format
		const outputDateString = `${inputDate.getUTCFullYear()}-${(inputDate.getUTCMonth() + 1).toString().padStart(2, '0')}-${inputDate.getUTCDate().toString().padStart(2, '0')} ${inputDate.getUTCHours().toString().padStart(2, '0')}:${inputDate.getUTCMinutes().toString().padStart(2, '0')}:${inputDate.getUTCSeconds().toString().padStart(2, '0')}`;

		return outputDateString;
	}

	let inputValue = '';

	function searchInput(value) {
		inputValue = value;
	}
	function onSubmit() {
		fetchData(currentPage);
    fetchUniqueValues();
	}

	function handlePrevious(total_page) {
		if (currentPage - 1 > 0) {
			pagenum = pagenum - 1;
			currentPage = currentPage - 1;
			console.log(currentPage, 'currentPageprevious');
			fetchData(currentPage);
			if (total_page > 0 && total_page != 0 && first_per_page > 5) {
				if (first_per_page <= last_per_page) {
					first_per_page = first_per_page - items_per_page;
					last_per_page = last_per_page - items_per_page;
				}
			}
		}
	}
	function handleNext(total_page) {
		if (currentPage + 1 >= page_count && currentPage < total_page) {
			console.log('Next button clicked');
			pagenum = pagenum + 1;
			currentPage = currentPage + 1;
			console.log(currentPage, 'currentPagecurrentPage');
			fetchData(currentPage);

			if (initial_count <= total_page) {
				if (first_per_page < last_per_page) {
					first_per_page = first_per_page + items_per_page;
					last_per_page = last_per_page + items_per_page;
				}
				initial_count = initial_count + 1;
			}
		}
	}
	function handleLast(total_page) {
		currentPage = total_page;
		fetchData(total_page);
	}
	function handleFirst() {
		currentPage = first_page;
		fetchData(first_page);
	}

	let selectedCheckboxes = {};

	// Modify the handleCheckboxSelection function to handle individual checkbox state
	function handleCheckboxSelection(column, value) {
		if (!selectedCheckboxes[column]) {
			selectedCheckboxes[column] = [];
		}

		const index = selectedCheckboxes[column].indexOf(value);
		if (index === -1) {
			// If checkbox is checked, add the value to selectedCheckboxes
			selectedCheckboxes[column].push(value);
		} else {
			// If checkbox is unchecked, remove the value from selectedCheckboxes
			selectedCheckboxes[column].splice(index, 1);
		}

		// Check if there are any values left for the column
		if (selectedCheckboxes[column].length === 0) {
			// If no values left, delete the column from selectedCheckboxes
			delete selectedCheckboxes[column];
		}
		fetchData(currentPage);
	}

	onMount(() => {
		fetchData(currentPage);
    fetchUniqueValues();
	});
</script>

<div class="main-container">
	<div class="left-container">
		<h1>hai</h1>
	</div>
	<div class="right-container">
		<div class="inner-container">
			<div style="display: flex; align-items: center;gap: 10px;">
				<div>
					<input type="search" on:input={() => searchInput(event.target.value)} />
				</div>
				<div>
					<input
						type="datetime-local"
            bind:value={bindStartDate}
					/>
				</div>
				<div>
					<input
						type="datetime-local"
						bind:value={bindEndDate}
					/>
				</div>
				<div>
					<input type="submit" on:click={onSubmit} />
				</div>
			</div>
			{#if searchData != '' && inputValue != ''}
				<div class="table-style">
					<table>
						<thead>
							<tr class="header-style">
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="MSISDN">MSISDN</div>
										<div class="filter-icon">
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="SOURCE IP">SOURCE IP</div>
										<div class="filter-icon" on:click={() => toggleDropdown(2)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="SOURCE PORT">SOURCE PORT</div>
										<div class="filter-icon" on:click={() => toggleDropdown(3)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="OTHER IP">OTHER IP</div>
										<div class="filter-icon" on:click={() => toggleDropdown(4)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="OTHER PORT">OTHER PORT</div>
										<div class="filter-icon" on:click={() => toggleDropdown(5)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="CGID">CGID</div>
										<div class="filter-icon" on:click={() => toggleDropdown(6)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="COMPANY">COMPANY</div>
										<div class="filter-icon" on:click={() => toggleDropdown(7)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="DOMAIN">DOMAIN</div>
										<div class="filter-icon" on:click={() => toggleDropdown(8)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="VPN">VPN</div>
										<div class="filter-icon" on:click={() => toggleDropdown(9)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="START TIME">START TIME</div>
										<div class="filter-icon" on:click={() => toggleDropdown(10)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="END TIME">END TIME</div>
										<div class="filter-icon" on:click={() => toggleDropdown(11)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="DURATION">DURATION</div>
										<div class="filter-icon" on:click={() => toggleDropdown(12)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="UP LINK">UP LINK</div>
										<div class="filter-icon" on:click={() => toggleDropdown(13)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="DOWN LINK">DOWN LINK</div>
										<div class="filter-icon" on:click={() => toggleDropdown(14)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="IP TYPE">IP TYPE</div>
										<div class="filter-icon" on:click={() => toggleDropdown(15)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="HOME CIRCLE">HOME CIRCLE</div>
										<div class="filter-icon" on:click={() => toggleDropdown(16)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
								<th>
									<div class="header-align">
										<div class="ellipsis-fit" title="PROVIDER">PROVIDER</div>
										<div class="filter-icon" on:click={() => toggleDropdown(17)}>
											<img src="filter.svg" alt="" />
										</div>
									</div>
								</th>
							</tr>
							<tr>
								<td>
									{#if isDropdownOpen[1]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(1)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['msisdn']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.msisdn as msisdn_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('msisdn', msisdn_values)}
																checked={selectedCheckboxes['msisdn'] &&
																	selectedCheckboxes['msisdn'].includes(msisdn_values)}
															/>
															{msisdn_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[2]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(2)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['source_ip']}
												on:input={handleSearch}
											/>

											<div class="options-container">
												{#each uniqueResponseValues.source_ip as source_ip_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('source_ip', source_ip_values)}
																checked={selectedCheckboxes['source_ip'] &&
																	selectedCheckboxes['source_ip'].includes(source_ip_values)}
															/>
															{source_ip_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[3]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(3)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['source_port']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.source_port as source_port_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('source_port', source_port_values)}
																checked={selectedCheckboxes['source_port'] &&
																	selectedCheckboxes['source_port'].includes(source_port_values)}
															/>
															{source_port_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[4]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(4)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['destination_ip']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.destination_ip as destination_ip_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('destination_ip', destination_ip_values)}
																checked={selectedCheckboxes['destination_ip'] &&
																	selectedCheckboxes['destination_ip'].includes(
																		destination_ip_values
																	)}
															/>
															{destination_ip_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[5]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(5)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['destination_port']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.destination_port as destination_port_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection(
																		'destination_port',
																		destination_port_values
																	)}
																checked={selectedCheckboxes['destination_port'] &&
																	selectedCheckboxes['destination_port'].includes(
																		destination_port_values
																	)}
															/>
															{destination_port_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[6]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(6)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['cell_id']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.cell_id as cell_id_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('cell_id', cell_id_values)}
																checked={selectedCheckboxes['cell_id'] &&
																	selectedCheckboxes['cell_id'].includes(cell_id_values)}
															/>
															{cell_id_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[7]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(7)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['company']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.company as company_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('company', company_values)}
																checked={selectedCheckboxes['company'] &&
																	selectedCheckboxes['company'].includes(company_values)}
															/>
															{company_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[8]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(8)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['domain']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.domain as domain_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('domain', domain_values)}
																checked={selectedCheckboxes['domain'] &&
																	selectedCheckboxes['domain'].includes(domain_values)}
															/>
															{domain_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[9]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(9)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['service']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.service as service_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('service', service_values)}
																checked={selectedCheckboxes['service'] &&
																	selectedCheckboxes['service'].includes(service_values)}
															/>
															{service_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[10]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(10)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['time']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.time as time_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('time', convertToISO8601(time_values))}
																checked={selectedCheckboxes['time'] &&
																	selectedCheckboxes['time'].includes(convertToISO8601(time_values))}
															/>
															{convertToISO8601(time_values)}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[11]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(11)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['time_et']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.time_et as time_et_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('time_et', convertToISO8601(time_et_values))}
																checked={selectedCheckboxes['time_et'] &&
																	selectedCheckboxes['time_et'].includes(convertToISO8601(time_et_values))}
															/>
															{convertToISO8601(time_et_values)}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[12]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(12)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['duration']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.duration as duration_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('duration', duration_values)}
																checked={selectedCheckboxes['duration'] &&
																	selectedCheckboxes['duration'].includes(duration_values)}
															/>
															{duration_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[13]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(13)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['uplink_vol']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.uplink_vol as uplink_vol_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('uplink_vol', uplink_vol_values)}
																checked={selectedCheckboxes['uplink_vol'] &&
																	selectedCheckboxes['uplink_vol'].includes(uplink_vol_values)}
															/>
															{uplink_vol_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[14]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(14)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['downlink_vol']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.downlink_vol as downlink_vol_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('downlink_vol', downlink_vol_values)}
																checked={selectedCheckboxes['downlink_vol'] &&
																	selectedCheckboxes['downlink_vol'].includes(downlink_vol_values)}
															/>
															{downlink_vol_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[15]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(15)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['com_type']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.com_type as com_type_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('com_type', com_type_values)}
																checked={selectedCheckboxes['com_type'] &&
																	selectedCheckboxes['com_type'].includes(com_type_values)}
															/>
															{com_type_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[16]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(16)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['roaming']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.roaming as roaming_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() => handleCheckboxSelection('roaming', roaming_values)}
																checked={selectedCheckboxes['roaming'] &&
																	selectedCheckboxes['roaming'].includes(roaming_values)}
															/>
															{roaming_values}
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
								<td>
									{#if isDropdownOpen[17]}
										<div style="position: absolute;">
											<div
												on:click={() => toggleDropdown(17)}
												style="cursor:pointer; display: flex; justify-content: flex-end;"
											>
												<img src="close.svg" alt="close" />
											</div>
											<input
												type="search"
												bind:value={searchParams['provider']}
												on:input={handleSearch}
											/>
											<div class="options-container">
												{#each uniqueResponseValues.provider as provider_values}
													<ul class="list-style">
														<li>
															<input
																type="checkbox"
																on:change={() =>
																	handleCheckboxSelection('provider', provider_values)}
																checked={selectedCheckboxes['provider'] &&
																	selectedCheckboxes['provider'].includes(provider_values)}
															/>
															<label>{provider_values}</label>
														</li>
													</ul>
												{/each}
											</div>
										</div>
									{/if}
								</td>
							</tr>
						</thead>
						<tbody>
							{#each searchData as item, index}
								<tr>
									<td>{item.msisdn || ''}</td>
									<td>{item.source_ip || ''}</td>
									<td>{item.source_port || ''}</td>
									<td>{item.destination_ip || ''}</td>
									<td>{item.destination_port || ''}</td>
									<td>{item.cell_id || ''}</td>
									<td>{item.company || ''}</td>
									<td>{item.domain || ''}</td>
									<td>{item.service || ''}</td>
									<td>{convertToISO8601(item.time) || ''}</td>
									<td>{convertToISO8601(item.time_et) || ''}</td>
									<td></td>
									<td>{item.uplink_vol || ''}</td>
									<td>{item.downlink_vol || ''}</td>
									<td>{item.com_type || ''}</td>
									<td>{item.roaming || ''}</td>
									<td>{item.provider || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
				<div class="table-pagination">
					<div>
						<p>
							Total Count : {length} and Total Page : {total_page}
						</p>
					</div>
					<div>
						<button type="button" class="button-primary" on:click={() => handleFirst()}
							>First</button
						>
						<button type="button" class="button-primary" on:click={() => handlePrevious(total_page)}
							>Previous</button
						>
						<button type="button" class="button-primary" style="margin-left:4px; margin-right:4px"
							>{currentPage}</button
						>
						<button type="button" class="button-primary" on:click={() => handleNext(total_page)}>
							Next</button
						>
						<button type="button" class="button-primary" on:click={() => handleLast(total_page)}
							>Last</button
						>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.main-container {
		width: 100%; /* Subtract 30px padding on each side */
		height: 100vh;
		display: flex;
		font-family: sans-serif;
	}
	.left-container {
		width: 7rem;
		height: 100vh;
		background-color: black;
	}
	.right-container {
		width: calc(100% - 7rem); /* Adjusted to take up remaining space */
		height: 100vh;
		padding-right: 20px;
		padding-left: 20px;
	}
	table {
		width: 100%;
	}
	.inner-container {
		height: 100vh; /* Subtract padding space */
	}
	.table-style {
		height: 85vh;
		overflow-y: scroll;
		position: relative;
		border: 1px solid #d9d9d9;
		border-radius: 4px;
	}
	tbody,
	td,
	tfoot,
	th,
	thead,
	tr {
		border-color: rgb(217 217 217);
		border-style: none;
		border-width: 1px;
	}
	td,
	th {
		border: none;
		padding: 14px;
	}
	/* Apply alternate colors to table rows */
	tr:nth-child(even) {
		background-color: #d4eaf7; /* Light gray background color for even rows */
	}
	tr:nth-child(odd) {
		background-color: #ffffff; /* White background color for odd rows */
	}
	tr.header-style {
		background-color: #5cb2eb;
		color: white;
		font-size: 14px;
	}
	input[type='search'] {
		box-sizing: border-box;
		border: 1px solid #ccc;
		border-radius: 2px;
		font-size: 16px;
		background-color: white;
		background-image: url(/src/lib/images/icon-search.svg);
		background-position: 140px 5px;
		background-repeat: no-repeat;
		padding: 4px;
		outline: none;
		width: 170px;
	}
	th {
		text-align: center;
		font-size: 16px;
		position: relative; /* Ensure the relative positioning for the container */
	}
	thead {
		position: sticky;
		top: 0;
	}
	/* scrollbar */
	::-webkit-scrollbar {
		width: 5px;
		height: 5px;
	}

	::-webkit-scrollbar-track {
		-webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
		-webkit-border-radius: 10px;
		border-radius: 10px;
	}

	::-webkit-scrollbar-thumb {
		-webkit-border-radius: 10px;
		border-radius: 10px;
		background: rgba(255, 255, 255, 0.3);
		-webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
	}

	::-webkit-scrollbar-thumb:window-inactive {
		background: rgba(255, 255, 255, 0.3);
	}

	/* Pagination styling */
	.table-pagination {
		height: 5vh;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.button-primary {
		height: 36px;
		text-align: center;
		background-color: #5cb2eb;
		color: white;
		border-radius: 2px;
		border-bottom: #5cb2eb;
	}
	.button-primary:hover {
		background-color: white;
		color: #5cb2eb;
		border-bottom: #5cb2eb;
	}
  
	.filter-icon {
		cursor: pointer;
	}
	.options-container {
		max-height: 200px;
		overflow-y: auto;
		border: 1px solid #ccc;
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background-color: white;
		z-index: 1000;
	}
	.list-style {
		list-style: none;
	}
	.header-align {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 170px; /* Adjust this width as needed */
	}

	.ellipsis-fit {
		position: relative;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		width: fit-content;
		cursor: pointer;
	}
</style>
