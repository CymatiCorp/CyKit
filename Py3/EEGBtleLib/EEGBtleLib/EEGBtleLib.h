#pragma once

#ifdef EEGBTLELIB_EXPORTS
	#define EMOTIVBTLELIB_API	__declspec(dllexport)
#else
	#define EMOTIVBTLELIB_API	__declspec(dllimport)
#endif


extern "C" EMOTIVBTLELIB_API const wchar_t* get_bluetooth_id(void);

extern "C" EMOTIVBTLELIB_API void set_callback_func(void *);

extern "C" EMOTIVBTLELIB_API void set_error_func(void *);

extern "C" EMOTIVBTLELIB_API HANDLE btle_init(WCHAR *);

extern "C" EMOTIVBTLELIB_API void run_data_collection(HANDLE, const WCHAR **);

extern "C" EMOTIVBTLELIB_API void btle_disconnect(HANDLE);