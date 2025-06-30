export const resetObject = (object) => {
    Object.keys(object).forEach(key => object[key] = null)
}